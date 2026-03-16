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
            'email',
            'telefone',
            'endereco',
            'cidade',
            'estado',
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
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite as iniciais da cidade para buscar',
                'autocomplete': 'off',
                'list': 'cidade-opcoes',
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pessoa de contato'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações adicionais', 'rows': 3}),
        }

    def clean_itens_fornecidos(self):
        valor = (self.cleaned_data.get('itens_fornecidos') or '').strip()
        if not valor:
            return ''

        itens = [item.strip() for item in valor.split(',') if item.strip()]
        itens_unicos = []
        for item in itens:
            if item not in itens_unicos:
                itens_unicos.append(item)

        return ', '.join(itens_unicos)
