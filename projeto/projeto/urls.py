"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes.views import ClienteViewSet
from produtos.views import ProdutoViewSet
from fornecedores.views import FornecedorViewSet
from compras.views import CompraViewSet
from vendas.views import VendaViewSet

# Criar router para API
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'vendas', VendaViewSet)


def root_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

urlpatterns = [
    path('', root_redirect_view, name='root'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('clientes.urls')),
    path('produtos/', include('produtos.urls')),
    path('fornecedores/', include('fornecedores.urls')),
    path('compras/', include('compras.urls')),
    path('vendas/', include('vendas.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

