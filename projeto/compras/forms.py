from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Compra


class CompraForm(forms.ModelForm):
    produto_nome = forms.CharField(
        label='Produto',
        widget=forms.HiddenInput(),
        required=True,
        error_messages={'required': 'Selecione um produto antes de salvar.'},
    )

    class Meta:
        model = Compra
        fields = ['fornecedor', 'preco_compra', 'preco_venda', 'data_compra', 'quantidade']
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'preco_compra': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Preco de compra', 'step': '0.01', 'min': '0'}
            ),
            'preco_venda': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Preco de venda', 'step': '0.01', 'min': '0'}
            ),
            'data_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'produto_id', None):
            self.fields['produto_nome'].initial = self.instance.produto.nome

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=Compra.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=Compra.LIMITE_FUTURO_DIAS)
        self.fields['data_compra'].widget.attrs['min'] = data_minima.isoformat()
        self.fields['data_compra'].widget.attrs['max'] = data_maxima.isoformat()

    def clean_preco_compra(self):
        valor = self.cleaned_data.get('preco_compra')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preco de compra nao pode ser negativo.')
        return valor

    def clean_preco_venda(self):
        valor = self.cleaned_data.get('preco_venda')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preco de venda nao pode ser negativo.')
        return valor

    def clean_quantidade(self):
        valor = self.cleaned_data.get('quantidade')
        if valor is not None and valor < 0:
            raise forms.ValidationError('A quantidade não pode ser negativa.')
        return valor

    def clean_data_compra(self):
        data = self.cleaned_data.get('data_compra')
        if data is None:
            return data

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=Compra.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=Compra.LIMITE_FUTURO_DIAS)

        if data < data_minima:
            raise forms.ValidationError('A data da compra está muito no passado.')
        if data > data_maxima:
            raise forms.ValidationError('A data da compra está muito no futuro.')
        return data
