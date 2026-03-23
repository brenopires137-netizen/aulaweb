from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta
from produtos.models import Produto
from fornecedores.models import Fornecedor


class Compra(models.Model):
    LIMITE_PASSADO_DIAS = 3650
    LIMITE_FUTURO_DIAS = 365

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name='Fornecedor')
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preco de compra')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preco de venda')
    data_compra = models.DateField(verbose_name='Data da Compra')
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
        ids_existentes = list(
            cls.objects.select_for_update().order_by('id').values_list('id', flat=True)
        )
        if not ids_existentes:
            return

        proximo_id = ids_existentes[0]
        for id_atual in ids_existentes:
            if id_atual != proximo_id:
                cls.objects.filter(id=id_atual).update(id=proximo_id)
            proximo_id += 1

    def clean(self):
        if self.preco_compra is not None and self.preco_compra < 0:
            raise ValidationError({'preco_compra': 'O preco de compra nao pode ser negativo.'})
        if self.preco_venda is not None and self.preco_venda < 0:
            raise ValidationError({'preco_venda': 'O preco de venda nao pode ser negativo.'})
        if self.quantidade is not None and self.quantidade < 0:
            raise ValidationError({'quantidade': 'A quantidade não pode ser negativa.'})
        if self.data_compra is not None:
            hoje = timezone.localdate()
            data_minima = hoje - timedelta(days=self.LIMITE_PASSADO_DIAS)
            data_maxima = hoje + timedelta(days=self.LIMITE_FUTURO_DIAS)
            if self.data_compra < data_minima:
                raise ValidationError({'data_compra': 'A data da compra está muito no passado.'})
            if self.data_compra > data_maxima:
                raise ValidationError({'data_compra': 'A data da compra está muito no futuro.'})

    @staticmethod
    def _atualizar_preco_produto(produto, preco_compra, preco_venda):
        campos = []
        if produto.preco_compra != preco_compra:
            produto.preco_compra = preco_compra
            campos.append('preco_compra')
        if produto.preco_venda != preco_venda:
            produto.preco_venda = preco_venda
            campos.append('preco_venda')
        if produto.preco != preco_venda:
            produto.preco = preco_venda
            campos.append('preco')
        return campos

    @staticmethod
    def _remover_quantidade_produto(produto, quantidade):
        if produto.quantidade - quantidade < 0:
            raise ValidationError('Não é possível concluir a operação pois o estoque ficaria negativo.')
        produto.quantidade -= quantidade
        produto.save(update_fields=['quantidade'])

    def _aplicar_no_produto(self):
        produto = Produto.objects.select_for_update().get(pk=self.produto_id)
        campos = self._atualizar_preco_produto(produto, self.preco_compra, self.preco_venda)
        produto.quantidade += self.quantidade
        campos.append('quantidade')
        
        # Atualizar data de compra
        produto.data_compra = self.data_compra
        campos.append('data_compra')
        
        # Calcular e atualizar data de validade usando o prazo do produto
        data_validade = self.data_compra + timedelta(days=produto.prazo_validade_dias)
        produto.data_validade = data_validade
        campos.append('data_validade')
        
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

            if not is_novo:
                compra_anterior = Compra.objects.select_for_update().get(pk=self.pk)

                if compra_anterior.confirmada and not self.confirmada:
                    raise ValidationError('Uma compra confirmada não pode voltar para em confirmação.')

                if not compra_anterior.confirmada and self.confirmada:
                    if not self.confirmado_em:
                        self.confirmado_em = timezone.now()
                    self._aplicar_no_produto()

                elif compra_anterior.confirmada and self.confirmada:
                    if compra_anterior.produto_id == self.produto_id:
                        produto = Produto.objects.select_for_update().get(pk=self.produto_id)
                        campos = self._atualizar_preco_produto(produto, self.preco_compra, self.preco_venda)
                        diferenca = self.quantidade - compra_anterior.quantidade
                        if diferenca != 0:
                            if produto.quantidade + diferenca < 0:
                                raise ValidationError('Não é possível concluir a operação pois o estoque ficaria negativo.')
                            produto.quantidade += diferenca
                            campos.append('quantidade')
                        if campos:
                            produto.save(update_fields=campos)
                    else:
                        produto_antigo = Produto.objects.select_for_update().get(pk=compra_anterior.produto_id)
                        self._remover_quantidade_produto(produto_antigo, compra_anterior.quantidade)
                        self._aplicar_no_produto()

            super().save(*args, **kwargs)

    def confirmar(self):
        with transaction.atomic():
            compra = Compra.objects.select_for_update().get(pk=self.pk)
            if compra.confirmada:
                return False

            compra.confirmada = True
            compra.confirmado_em = timezone.now()
            compra._aplicar_no_produto()
            Compra.objects.filter(pk=compra.pk).update(
                confirmada=True,
                confirmado_em=compra.confirmado_em,
            )
            self.confirmada = True
            self.confirmado_em = compra.confirmado_em
            return True

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.confirmada:
                produto = Produto.objects.select_for_update().get(pk=self.produto_id)
                self._remover_quantidade_produto(produto, self.quantidade)
            resultado = super().delete(*args, **kwargs)

            # Reorganiza os IDs para remover buracos na sequência.
            Compra._normalizar_ids()
            return resultado

    def __str__(self):
        return f'Compra #{self.pk} - {self.produto}'

    class Meta:
        ordering = ['-data_compra']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
