from django.urls import path

from .views import (
    VendaConfirmarTodasView,
    VendaConfirmarView,
    VendaCreateView,
    VendaDeleteView,
    VendaDetailView,
    VendaListView,
    VendaUpdateView,
)

urlpatterns = [
    path('', VendaListView.as_view(), name='vendas_lista'),
    path('nova/', VendaCreateView.as_view(), name='vendas_criar'),
    path('detalhes/<int:pk>/', VendaDetailView.as_view(), name='vendas_detalhes'),
    path('editar/<int:pk>/', VendaUpdateView.as_view(), name='vendas_editar'),
    path('excluir/<int:pk>/', VendaDeleteView.as_view(), name='vendas_excluir'),
    path('confirmar/<int:pk>/', VendaConfirmarView.as_view(), name='vendas_confirmar'),
    path('confirmar-todas/', VendaConfirmarTodasView.as_view(), name='vendas_confirmar_todas'),
]
