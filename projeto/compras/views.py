from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from decimal import Decimal
from rest_framework import viewsets
from .forms import CompraForm
from .models import Compra
from .serializers import CompraSerializer
from fornecedores.models import Fornecedor
from produtos.models import Produto


def _get_or_create_produto(nome):
    nome_limpo = (nome or '').strip()
    if not nome_limpo:
        return None
    qs = Produto.objects.filter(nome__iexact=nome_limpo)
    if qs.exists():
        return qs.first()
    return Produto.objects.create(nome=nome_limpo, preco=Decimal('0.00'), quantidade=0)


class CompraListView(ListView):
    model = Compra
    template_name = 'compras/lista.html'
    context_object_name = 'compras'

    def get_queryset(self):
        return Compra.objects.order_by('id')


class CompraCreateView(CreateView):
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
        produto = _get_or_create_produto(form.cleaned_data.get('produto_nome'))
        form.instance.produto = produto
        return super().form_valid(form)


class CompraUpdateView(UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/form.html'
    success_url = reverse_lazy('compras_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens_por_fornecedor'] = CompraCreateView._mapa_itens_fornecedor()
        return context

    def form_valid(self, form):
        produto = _get_or_create_produto(form.cleaned_data.get('produto_nome'))
        form.instance.produto = produto
        return super().form_valid(form)


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'compras/excluir.html'
    success_url = reverse_lazy('compras_lista')


class CompraDetailView(DetailView):
    model = Compra
    template_name = 'compras/detalhes.html'
    context_object_name = 'compra'


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
