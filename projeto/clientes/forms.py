# clientes/forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "telefone"]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com',
                'type': 'email',
                'title': 'Digite um email válido'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 0000-0000',
                'maxlength': '15',
                'pattern': r'\(\d{2}\) \d{4,5}-\d{4}',
                'title': 'Telefone no formato (00) 0000-0000 ou (00) 00000-0000'
            }),
        }