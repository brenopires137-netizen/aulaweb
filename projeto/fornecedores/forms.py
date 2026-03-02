from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'nome_fantasia',
            'razao_social',
            'cnpj',
            'tipo_fornecimento',
            'categorias_fornecidas',
            'itens_fornecidos',
            'condicao_pagamento',
            'email',
            'telefone',
            'endereco',
            'contato',
            'observacoes',
        ]
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome fantasia'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão social'}),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '00.000.000/0000-00',
                'maxlength': '18',
                'pattern': r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',
                'title': 'CNPJ no formato 00.000.000/0000-00'
            }),
            'tipo_fornecimento': forms.Select(attrs={'class': 'form-control'}),
            'categorias_fornecidas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: alimentos, limpeza, elétrica'}),
            'itens_fornecidos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva produtos/serviços fornecidos', 'rows': 3}),
            'condicao_pagamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 30/60 dias, boleto, PIX'}),
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
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pessoa de contato'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações adicionais', 'rows': 3}),
        }
