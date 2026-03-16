from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao', 'quantidade', 'preco_compra', 'preco_venda', 'data_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço', 'step': '0.01', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 4}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': '0'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de compra', 'step': '0.01', 'min': '0'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de venda', 'step': '0.01', 'min': '0'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_preco(self):
        valor = self.cleaned_data.get('preco')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preço não pode ser negativo.')
        return valor

    def clean_quantidade(self):
        valor = self.cleaned_data.get('quantidade')
        if valor is not None and valor < 0:
            raise forms.ValidationError('A quantidade não pode ser negativa.')
        return valor

    def clean_preco_compra(self):
        valor = self.cleaned_data.get('preco_compra')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preço de compra não pode ser negativo.')
        return valor

    def clean_preco_venda(self):
        valor = self.cleaned_data.get('preco_venda')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preço de venda não pode ser negativo.')
        return valor
