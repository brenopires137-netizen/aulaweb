from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import FornecedorForm
from .models import Fornecedor
from .serializers import FornecedorSerializer
from produtos.models import Produto


class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedores/lista.html'
    context_object_name = 'fornecedores'


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form.html'
    success_url = reverse_lazy('fornecedores_lista')

    @staticmethod
    def _montar_itens_sugestao():
        sugestoes = set(
            Produto.objects.order_by('nome').values_list('nome', flat=True)
        )

        itens_fornecedores = Fornecedor.objects.exclude(
            itens_fornecidos__isnull=True
        ).exclude(
            itens_fornecidos=''
        ).values_list('itens_fornecidos', flat=True)

        for texto_itens in itens_fornecedores:
            for item in texto_itens.split(','):
                item_limpo = item.strip()
                if item_limpo:
                    sugestoes.add(item_limpo)

        return sorted(sugestoes, key=lambda nome: nome.lower())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos_disponiveis'] = self._montar_itens_sugestao()
        return context


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form.html'
    success_url = reverse_lazy('fornecedores_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos_disponiveis'] = FornecedorCreateView._montar_itens_sugestao()
        return context


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'fornecedores/excluir.html'
    success_url = reverse_lazy('fornecedores_lista')


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer

    @action(detail=False, methods=['get'])
    def por_cnpj(self, request):
        cnpj = request.query_params.get('cnpj')
        if cnpj is None:
            return Response({'error': 'CNPJ não fornecido'}, status=400)

        fornecedores = Fornecedor.objects.filter(cnpj=cnpj)
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)
