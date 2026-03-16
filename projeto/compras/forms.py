from django import forms
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
        fields = ['fornecedor', 'preco', 'data_compra', 'quantidade']
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço', 'step': '0.01', 'min': '0'}),
            'data_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'produto_id', None):
            self.fields['produto_nome'].initial = self.instance.produto.nome

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
