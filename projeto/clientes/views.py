from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cliente
from .forms import ClienteForm
from .serializers import ClienteSerializer
from produtos.models import Produto
from fornecedores.models import Fornecedor
from compras.models import Compra
from vendas.models import Venda

# clientes/views.py

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "clientes/lista.html"
    context_object_name = "clientes"

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("lista")

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("lista")

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "clientes/excluir.html"
    success_url = reverse_lazy("lista")

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        produtos_confirmados_ids = (
            Compra.objects.filter(confirmada=True)
            .values_list('produto_id', flat=True)
            .distinct()
        )

        context['total_clientes'] = Cliente.objects.count()
        context['total_produtos'] = Produto.objects.filter(id__in=produtos_confirmados_ids).count()
        context['total_estoque_geral'] = (
            Produto.objects.filter(id__in=produtos_confirmados_ids).aggregate(total=Sum('quantidade'))['total'] or 0
        )
        context['total_fornecedores'] = Fornecedor.objects.count()
        context['total_vendas_confirmadas'] = Venda.objects.filter(confirmada=True).count()
        context['total_vendas_pendentes'] = Venda.objects.filter(confirmada=False).count()
        context['total_itens_vendidos'] = (
            Venda.objects.filter(confirmada=True).aggregate(total=Sum('quantidade'))['total'] or 0
        )

        return context

# ViewSet para API REST
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=False, methods=['get'])
    def por_email(self, request):
        """Buscar clientes por email"""
        email = request.query_params.get('email', None)
        if email is not None:
            clientes = Cliente.objects.filter(email=email)
            serializer = self.get_serializer(clientes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email não fornecido'}, status=400)