from django.urls import path
from .views import (
    FornecedorListView,
    FornecedorCreateView,
    FornecedorUpdateView,
    FornecedorDeleteView,
)


urlpatterns = [
    path('', FornecedorListView.as_view(), name='fornecedores_lista'),
    path('novo/', FornecedorCreateView.as_view(), name='fornecedores_criar'),
    path('editar/<int:pk>/', FornecedorUpdateView.as_view(), name='fornecedores_editar'),
    path('excluir/<int:pk>/', FornecedorDeleteView.as_view(), name='fornecedores_excluir'),
]
