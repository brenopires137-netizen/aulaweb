from rest_framework import serializers
from .models import Fornecedor


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = [
            'id',
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
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
