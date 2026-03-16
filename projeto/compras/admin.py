from django.contrib import admin
from .models import Compra


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('pk', 'produto', 'fornecedor', 'preco', 'quantidade', 'data_compra')
    list_filter = ('fornecedor', 'data_compra')
    search_fields = ('produto__nome', 'fornecedor__nome_fantasia')
