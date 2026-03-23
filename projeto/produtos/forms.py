from django import forms
from datetime import timedelta
from django.utils import timezone
from .models import Produto

class ProdutoForm(forms.ModelForm):
    LIMITE_PASSADO_DIAS = 3650
    LIMITE_FUTURO_DIAS = 365

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'quantidade', 'preco_compra', 'preco_venda', 'data_compra']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 4}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': '1'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de compra', 'step': '0.01', 'min': '0'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de venda', 'step': '0.01', 'min': '0'}),
            'data_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preco_venda'].required = True

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=self.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=self.LIMITE_FUTURO_DIAS)
        self.fields['data_compra'].widget.attrs['min'] = data_minima.isoformat()
        self.fields['data_compra'].widget.attrs['max'] = data_maxima.isoformat()

    def clean_quantidade(self):
        valor = self.cleaned_data.get('quantidade')
        if valor is None:
            return valor

        if self.instance.pk is None and valor <= 0:
            raise forms.ValidationError('Ao adicionar um produto, a quantidade deve ser maior que 0.')

        if valor < 0:
            raise forms.ValidationError('A quantidade não pode ser negativa.')

        return valor

    def clean_preco_compra(self):
        valor = self.cleaned_data.get('preco_compra')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preço de compra não pode ser negativo.')
        return valor

    def clean_preco_venda(self):
        valor = self.cleaned_data.get('preco_venda')
        if valor is None:
            raise forms.ValidationError('O preço de venda é obrigatório.')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preço de venda não pode ser negativo.')
        return valor

    def clean_data_compra(self):
        data = self.cleaned_data.get('data_compra')
        if data is None:
            return data

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=self.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=self.LIMITE_FUTURO_DIAS)

        if data < data_minima:
            raise forms.ValidationError('A data da compra está muito no passado.')
        if data > data_maxima:
            raise forms.ValidationError('A data da compra está muito no futuro.')
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.preco = self.cleaned_data.get('preco_venda')
        if instance.data_compra:
            instance.data_validade = instance.data_compra + timedelta(days=instance.prazo_validade_dias)
        if commit:
            instance.save()
        return instance

