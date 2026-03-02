from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cliente
from .forms import ClienteForm
from .serializers import ClienteSerializer

# clientes/views.py

class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/lista.html"
    context_object_name = "clientes"

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("lista")

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("lista")

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes/excluir.html"
    success_url = reverse_lazy("lista")

class HomeView(TemplateView):
    template_name = "home.html"

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