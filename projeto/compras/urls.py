from django.urls import path
from .views import CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView, CompraDetailView

urlpatterns = [
    path('', CompraListView.as_view(), name='compras_lista'),
    path('nova/', CompraCreateView.as_view(), name='compras_criar'),
    path('detalhes/<int:pk>/', CompraDetailView.as_view(), name='compras_detalhes'),
    path('editar/<int:pk>/', CompraUpdateView.as_view(), name='compras_editar'),
    path('excluir/<int:pk>/', CompraDeleteView.as_view(), name='compras_excluir'),
]
