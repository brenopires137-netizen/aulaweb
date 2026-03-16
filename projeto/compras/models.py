from django.core.exceptions import ValidationError
from django.db import models, transaction
from produtos.models import Produto
from fornecedores.models import Fornecedor


class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name='Fornecedor')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    data_compra = models.DateField(verbose_name='Data da Compra')
    quantidade = models.IntegerField(verbose_name='Quantidade')
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
        if self.preco is not None and self.preco < 0:
            raise ValidationError({'preco': 'O preço não pode ser negativo.'})
        if self.quantidade is not None and self.quantidade < 0:
            raise ValidationError({'quantidade': 'A quantidade não pode ser negativa.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        is_novo = self._state.adding

        with transaction.atomic():
            if is_novo and not self.pk:
                self.pk = self._proximo_id_por_sequencia()

            if not is_novo:
                compra_anterior = Compra.objects.select_for_update().get(pk=self.pk)

                if compra_anterior.produto_id == self.produto_id:
                    diferenca = self.quantidade - compra_anterior.quantidade
                    if diferenca != 0:
                        self.produto.quantidade += diferenca
                        self.produto.save(update_fields=['quantidade'])
                else:
                    compra_anterior.produto.quantidade -= compra_anterior.quantidade
                    compra_anterior.produto.save(update_fields=['quantidade'])

                    self.produto.quantidade += self.quantidade
                    self.produto.save(update_fields=['quantidade'])
            else:
                self.produto.quantidade += self.quantidade
                self.produto.save(update_fields=['quantidade'])

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.produto.quantidade - self.quantidade < 0:
                raise ValidationError('Não é possível excluir esta compra pois o estoque ficaria negativo.')

            self.produto.quantidade -= self.quantidade
            self.produto.save(update_fields=['quantidade'])
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
