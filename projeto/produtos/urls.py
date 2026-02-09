from django.urls import path
from .views import (
    ProdutoListView,
    ProdutoCreateView,
    ProdutoUpdateView,
    ProdutoDeleteView
)

urlpatterns = [
    path("", ProdutoListView.as_view(), name="produtos_lista"),
    path("novo/", ProdutoCreateView.as_view(), name="produtos_criar"),
    path("editar/<int:pk>/", ProdutoUpdateView.as_view(), name="produtos_editar"),
    path("excluir/<int:pk>/", ProdutoDeleteView.as_view(), name="produtos_excluir"),
]
