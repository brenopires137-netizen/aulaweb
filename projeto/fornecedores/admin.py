from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = (
        'nome_fantasia',
        'cnpj',
        'tipo_fornecimento',
        'categorias_fornecidas',
        'cidade',
        'estado',
        'contato',
        'telefone',
    )
    search_fields = (
        'nome_fantasia',
        'razao_social',
        'cnpj',
        'categorias_fornecidas',
        'itens_fornecidos',
        'email',
        'cidade',
        'estado',
    )
    list_filter = ('tipo_fornecimento', 'estado')
