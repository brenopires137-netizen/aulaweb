from django.db import models


class Fornecedor(models.Model):
    class TipoFornecimento(models.TextChoices):
        PRODUTOS = 'PRODUTOS', 'Produtos'
        SERVICOS = 'SERVICOS', 'Serviços'
        AMBOS = 'AMBOS', 'Produtos e Serviços'

    nome_fantasia = models.CharField(max_length=120)
    razao_social = models.CharField(max_length=160, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    tipo_fornecimento = models.CharField(
        max_length=20,
        choices=TipoFornecimento.choices,
        default=TipoFornecimento.PRODUTOS,
    )
    categorias_fornecidas = models.CharField(max_length=200, blank=True, null=True)
    itens_fornecidos = models.TextField(blank=True, null=True)
    condicao_pagamento = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    contato = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        ordering = ['nome_fantasia']
