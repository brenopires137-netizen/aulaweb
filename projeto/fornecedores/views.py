from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import FornecedorForm
from .models import Fornecedor
from .serializers import FornecedorSerializer


class FornecedorListView(ListView):
    model = Fornecedor
    template_name = 'fornecedores/lista.html'
    context_object_name = 'fornecedores'


class FornecedorCreateView(CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form.html'
    success_url = reverse_lazy('fornecedores_lista')


class FornecedorUpdateView(UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form.html'
    success_url = reverse_lazy('fornecedores_lista')


class FornecedorDeleteView(DeleteView):
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
