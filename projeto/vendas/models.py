from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from clientes.models import Cliente
from produtos.models import Produto


class Venda(models.Model):
    LIMITE_PASSADO_DIAS = 3650
    LIMITE_FUTURO_DIAS = 365

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preco unitario')
    data_venda = models.DateField(verbose_name='Data da venda')
    quantidade = models.IntegerField(verbose_name='Quantidade')
    confirmada = models.BooleanField(default=False, verbose_name='Confirmada')
    confirmado_em = models.DateTimeField(null=True, blank=True, verbose_name='Confirmado em')
    criado_em = models.DateTimeField(auto_now_add=True)

    @classmethod
    def _proximo_id_por_sequencia(cls):
        ultimo_id = cls.objects.select_for_update().order_by('-id').values_list('id', flat=True).first()
        if ultimo_id is None:
            return 1
        return ultimo_id + 1

    @classmethod
    def _normalizar_ids(cls):
        ids_existentes = list(cls.objects.select_for_update().order_by('id').values_list('id', flat=True))
        if not ids_existentes:
            return

        proximo_id = ids_existentes[0]
        for id_atual in ids_existentes:
            if id_atual != proximo_id:
                cls.objects.filter(id=id_atual).update(id=proximo_id)
            proximo_id += 1

    def clean(self):
        if self.preco_unitario is not None and self.preco_unitario < 0:
            raise ValidationError({'preco_unitario': 'O preco nao pode ser negativo.'})
        if self.quantidade is not None and self.quantidade <= 0:
            raise ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})

        if self.data_venda is not None:
            hoje = timezone.localdate()
            data_minima = hoje - timedelta(days=self.LIMITE_PASSADO_DIAS)
            data_maxima = hoje + timedelta(days=self.LIMITE_FUTURO_DIAS)
            if self.data_venda < data_minima:
                raise ValidationError({'data_venda': 'A data da venda esta muito no passado.'})
            if self.data_venda > data_maxima:
                raise ValidationError({'data_venda': 'A data da venda esta muito no futuro.'})

        if self.produto_id is not None and self.quantidade is not None:
            produto = Produto.objects.filter(pk=self.produto_id).first()
            if produto is not None:
                if self._state.adding:
                    if self.quantidade > produto.quantidade:
                        raise ValidationError(
                            {'quantidade': f'Estoque insuficiente. Disponivel: {produto.quantidade}.'}
                        )
                    return

                venda_anterior = Venda.objects.filter(pk=self.pk).first()
                if venda_anterior is None:
                    if self.quantidade > produto.quantidade:
                        raise ValidationError(
                            {'quantidade': f'Estoque insuficiente. Disponivel: {produto.quantidade}.'}
                        )
                    return

                if not venda_anterior.confirmada:
                    if self.quantidade > produto.quantidade:
                        raise ValidationError(
                            {'quantidade': f'Estoque insuficiente. Disponivel: {produto.quantidade}.'}
                        )
                elif self.confirmada:
                    if venda_anterior.produto_id == self.produto_id:
                        diferenca = self.quantidade - venda_anterior.quantidade
                        if diferenca > produto.quantidade:
                            raise ValidationError(
                                {'quantidade': f'Estoque insuficiente. Disponivel: {produto.quantidade}.'}
                            )
                    elif self.quantidade > produto.quantidade:
                        raise ValidationError(
                            {'quantidade': f'Estoque insuficiente. Disponivel: {produto.quantidade}.'}
                        )

    @staticmethod
    def _atualizar_preco_produto(produto, preco_unitario):
        campos = []
        if produto.preco != preco_unitario:
            produto.preco = preco_unitario
            campos.append('preco')
        if produto.preco_venda != preco_unitario:
            produto.preco_venda = preco_unitario
            campos.append('preco_venda')
        return campos

    @staticmethod
    def _adicionar_quantidade_produto(produto, quantidade):
        produto.quantidade += quantidade
        produto.save(update_fields=['quantidade'])

    @staticmethod
    def _remover_quantidade_produto(produto, quantidade):
        if produto.quantidade - quantidade < 0:
            raise ValidationError('Nao e possivel concluir a operacao pois o estoque ficaria negativo.')
        produto.quantidade -= quantidade
        produto.save(update_fields=['quantidade'])

    def _aplicar_no_produto(self):
        produto = Produto.objects.select_for_update().get(pk=self.produto_id)
        campos = self._atualizar_preco_produto(produto, self.preco_unitario)
        if produto.quantidade - self.quantidade < 0:
            raise ValidationError('Nao e possivel confirmar a venda sem estoque suficiente.')
        produto.quantidade -= self.quantidade
        campos.append('quantidade')
        produto.save(update_fields=campos)

    def save(self, *args, **kwargs):
        self.full_clean()
        is_novo = self._state.adding

        with transaction.atomic():
            if is_novo and not self.pk:
                self.pk = self._proximo_id_por_sequencia()

            if is_novo:
                if self.confirmada and not self.confirmado_em:
                    self.confirmado_em = timezone.now()
                    self._aplicar_no_produto()
                super().save(*args, **kwargs)
                return

            venda_anterior = Venda.objects.select_for_update().get(pk=self.pk)

            if venda_anterior.confirmada and not self.confirmada:
                raise ValidationError('Uma venda confirmada nao pode voltar para em confirmacao.')

            if not venda_anterior.confirmada and self.confirmada:
                if not self.confirmado_em:
                    self.confirmado_em = timezone.now()
                self._aplicar_no_produto()

            elif venda_anterior.confirmada and self.confirmada:
                if venda_anterior.produto_id == self.produto_id:
                    produto = Produto.objects.select_for_update().get(pk=self.produto_id)
                    campos = self._atualizar_preco_produto(produto, self.preco_unitario)
                    diferenca = self.quantidade - venda_anterior.quantidade
                    if diferenca > 0:
                        self._remover_quantidade_produto(produto, diferenca)
                    elif diferenca < 0:
                        self._adicionar_quantidade_produto(produto, abs(diferenca))
                    if diferenca != 0:
                        campos.append('quantidade')
                    if campos:
                        produto.save(update_fields=list(set(campos)))
                else:
                    produto_antigo = Produto.objects.select_for_update().get(pk=venda_anterior.produto_id)
                    self._adicionar_quantidade_produto(produto_antigo, venda_anterior.quantidade)
                    self._aplicar_no_produto()

            super().save(*args, **kwargs)

    def confirmar(self):
        with transaction.atomic():
            venda = Venda.objects.select_for_update().get(pk=self.pk)
            if venda.confirmada:
                return False

            venda.confirmada = True
            venda.confirmado_em = timezone.now()
            venda._aplicar_no_produto()
            Venda.objects.filter(pk=venda.pk).update(
                confirmada=True,
                confirmado_em=venda.confirmado_em,
            )
            self.confirmada = True
            self.confirmado_em = venda.confirmado_em
            return True

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.confirmada:
                produto = Produto.objects.select_for_update().get(pk=self.produto_id)
                self._adicionar_quantidade_produto(produto, self.quantidade)

            resultado = super().delete(*args, **kwargs)
            Venda._normalizar_ids()
            return resultado

    def __str__(self):
        return f'Venda #{self.pk} - {self.produto}'

    class Meta:
        ordering = ['-data_venda']
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
