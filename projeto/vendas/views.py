from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import viewsets

from .forms import VendaForm
from .models import Venda
from .serializers import VendaSerializer


class VendaListView(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'vendas/lista.html'
    context_object_name = 'vendas_confirmadas'

    def get_queryset(self):
        return Venda.objects.filter(confirmada=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendas_pendentes'] = Venda.objects.filter(confirmada=False).order_by('id')
        return context


class VendaCreateView(LoginRequiredMixin, CreateView):
    model = Venda
    form_class = VendaForm
    template_name = 'vendas/form.html'
    success_url = reverse_lazy('vendas_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['precos_por_produto'] = {
            str(produto.id): str(produto.preco_venda or produto.preco or 0)
            for produto in form.fields['produto'].queryset
        }
        return context


class VendaUpdateView(LoginRequiredMixin, UpdateView):
    model = Venda
    form_class = VendaForm
    template_name = 'vendas/form.html'
    success_url = reverse_lazy('vendas_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['precos_por_produto'] = {
            str(produto.id): str(produto.preco_venda or produto.preco or 0)
            for produto in form.fields['produto'].queryset
        }
        return context


class VendaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = 'vendas/excluir.html'
    success_url = reverse_lazy('vendas_lista')


class VendaDetailView(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = 'vendas/detalhes.html'
    context_object_name = 'venda'


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer


class VendaConfirmarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk)
        venda.confirmar()
        return redirect('vendas_lista')


class VendaConfirmarTodasView(LoginRequiredMixin, View):
    def post(self, request):
        for venda in Venda.objects.filter(confirmada=False).order_by('id'):
            venda.confirmar()
        return redirect('vendas_lista')
