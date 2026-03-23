from django.contrib import admin
from .models import Venda


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cliente', 'produto', 'preco_unitario', 'quantidade', 'data_venda', 'confirmada')
    list_filter = ('confirmada', 'cliente', 'data_venda')
    search_fields = ('cliente__nome', 'produto__nome')
