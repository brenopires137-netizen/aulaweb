# clientes/urls.py
from django.urls import path
from . import views
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
    HomeView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clientes/", ClienteListView.as_view(), name="lista"),
    path("clientes/novo/", ClienteCreateView.as_view(), name="criar"),
    path("clientes/editar/<int:pk>/", ClienteUpdateView.as_view(), name="editar"),
    path("clientes/excluir/<int:pk>/", ClienteDeleteView.as_view(), name="excluir"),
]