from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao', 'quantidade', 'preco_compra', 'preco_venda', 'data_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço', 'step': '0.01'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 4}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de compra', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de venda', 'step': '0.01'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
