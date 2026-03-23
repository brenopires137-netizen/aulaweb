from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from decimal import Decimal
from rest_framework import viewsets
from .forms import CompraForm
from .models import Compra
from .serializers import CompraSerializer
from fornecedores.models import Fornecedor
from produtos.models import Produto


def _get_or_create_produto(nome, preco_compra=None, preco_venda=None):
    nome_limpo = (nome or '').strip()
    if not nome_limpo:
        return None
    qs = Produto.objects.filter(nome__iexact=nome_limpo)
    if qs.exists():
        return qs.first()
    preco_compra_inicial = preco_compra if preco_compra is not None else Decimal('0.00')
    preco_venda_inicial = preco_venda if preco_venda is not None else Decimal('0.00')
    return Produto.objects.create(
        nome=nome_limpo,
        preco=preco_venda_inicial,
        preco_compra=preco_compra_inicial,
        preco_venda=preco_venda_inicial,
        quantidade=0,
    )


class CompraListView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = 'compras/lista.html'
    context_object_name = 'compras_confirmadas'

    def get_queryset(self):
        return Compra.objects.filter(confirmada=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compras_pendentes'] = Compra.objects.filter(confirmada=False).order_by('id')
        return context


class CompraCreateView(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/form.html'
    success_url = reverse_lazy('compras_lista')

    @staticmethod
    def _mapa_itens_fornecedor():
        mapa = {}
        fornecedores = Fornecedor.objects.values('id', 'itens_fornecidos')

        for fornecedor in fornecedores:
            itens_texto = (fornecedor['itens_fornecidos'] or '').strip()
            if not itens_texto:
                mapa[str(fornecedor['id'])] = []
                continue

            itens = []
            for item in itens_texto.split(','):
                item_limpo = item.strip()
                if item_limpo and item_limpo not in itens:
                    itens.append(item_limpo)
            mapa[str(fornecedor['id'])] = itens

        return mapa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens_por_fornecedor'] = self._mapa_itens_fornecedor()
        return context

    def form_valid(self, form):
        produto = _get_or_create_produto(
            form.cleaned_data.get('produto_nome'),
            form.cleaned_data.get('preco_compra'),
            form.cleaned_data.get('preco_venda'),
        )
        form.instance.produto = produto
        return super().form_valid(form)


class CompraUpdateView(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/form.html'
    success_url = reverse_lazy('compras_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens_por_fornecedor'] = CompraCreateView._mapa_itens_fornecedor()
        return context

    def form_valid(self, form):
        produto = _get_or_create_produto(
            form.cleaned_data.get('produto_nome'),
            form.cleaned_data.get('preco_compra'),
            form.cleaned_data.get('preco_venda'),
        )
        form.instance.produto = produto
        return super().form_valid(form)


class CompraDeleteView(LoginRequiredMixin, DeleteView):
    model = Compra
    template_name = 'compras/excluir.html'
    success_url = reverse_lazy('compras_lista')


class CompraDetailView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = 'compras/detalhes.html'
    context_object_name = 'compra'


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer


class CompraConfirmarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        compra = get_object_or_404(Compra, pk=pk)
        compra.confirmar()
        return redirect('compras_lista')


class CompraConfirmarTodasView(LoginRequiredMixin, View):
    def post(self, request):
        for compra in Compra.objects.filter(confirmada=False).order_by('id'):
            compra.confirmar()
        return redirect('compras_lista')
