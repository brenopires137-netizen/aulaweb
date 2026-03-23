from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Venda


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'produto', 'preco_unitario', 'data_venda', 'quantidade']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'preco_unitario': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Preco unitario', 'step': '0.01', 'min': '0'}
            ),
            'data_venda': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Exibe produtos com estoque, incluindo itens criados manualmente.
        self.fields['produto'].queryset = self.fields['produto'].queryset.filter(quantidade__gt=0)
        self.fields['preco_unitario'].widget.attrs['readonly'] = True

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=Venda.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=Venda.LIMITE_FUTURO_DIAS)
        self.fields['data_venda'].widget.attrs['min'] = data_minima.isoformat()
        self.fields['data_venda'].widget.attrs['max'] = data_maxima.isoformat()

    def clean_preco_unitario(self):
        valor = self.cleaned_data.get('preco_unitario')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O preco nao pode ser negativo.')
        return valor

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')

        if produto is not None:
            cleaned_data['preco_unitario'] = produto.preco_venda or produto.preco or 0

        return cleaned_data

    def clean_quantidade(self):
        valor = self.cleaned_data.get('quantidade')
        if valor is not None and valor <= 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')
        return valor

    def clean_data_venda(self):
        data = self.cleaned_data.get('data_venda')
        if data is None:
            return data

        hoje = timezone.localdate()
        data_minima = hoje - timedelta(days=Venda.LIMITE_PASSADO_DIAS)
        data_maxima = hoje + timedelta(days=Venda.LIMITE_FUTURO_DIAS)

        if data < data_minima:
            raise forms.ValidationError('A data da venda esta muito no passado.')
        if data > data_maxima:
            raise forms.ValidationError('A data da venda esta muito no futuro.')
        return data
