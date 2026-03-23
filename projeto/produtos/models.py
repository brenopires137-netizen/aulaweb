from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.IntegerField(blank=True, default=0)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prazo_validade_dias = models.IntegerField(default=30, verbose_name='Prazo de Validade (dias)')
    data_compra = models.DateField(blank=True, null=True, verbose_name='Data da Última Compra')
    data_validade = models.DateField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-criado_em']
