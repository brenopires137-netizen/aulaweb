from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models import Q
from django.db.models import Exists, OuterRef
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produto
from .forms import ProdutoForm
from .serializers import ProdutoSerializer
from compras.models import Compra

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produtos/lista.html"
    context_object_name = "produtos"

    def get_queryset(self):
        compras_relacionadas = Compra.objects.filter(produto_id=OuterRef('pk'))
        return Produto.objects.filter(
            Q(compra__confirmada=True) | Q(compra__isnull=True)
        ).distinct().annotate(
            origem_aba_compras=Exists(compras_relacionadas)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_itens_comprados'] = (
            Compra.objects.filter(confirmada=True).aggregate(total=Sum('quantidade'))['total'] or 0
        )
        context['total_itens_adicionados'] = (
            Produto.objects.filter(compra__isnull=True).aggregate(total=Sum('quantidade'))['total'] or 0
        )
        context['total_estoque_geral'] = self.get_queryset().aggregate(total=Sum('quantidade'))['total'] or 0
        return context

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("produtos_lista")

class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("produtos_lista")

class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produtos/excluir.html"
    success_url = reverse_lazy("produtos_lista")

# ViewSet para API REST
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    @action(detail=False, methods=['get'])
    def em_estoque(self, request):
        """Listar produtos em estoque"""
        produtos = Produto.objects.filter(quantidade__gt=0)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sem_estoque(self, request):
        """Listar produtos fora de estoque"""
        produtos = Produto.objects.filter(quantidade__lte=0)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def atualizar_quantidade(self, request, pk=None):
        """Atualizar quantidade do produto"""
        produto = self.get_object()
        quantidade = request.data.get('quantidade')
        if quantidade is not None:
            produto.quantidade = quantidade
            produto.save()
            serializer = self.get_serializer(produto)
            return Response(serializer.data)
        return Response({'error': 'Quantidade não fornecida'}, status=400)