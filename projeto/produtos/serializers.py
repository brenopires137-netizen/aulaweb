from rest_framework import serializers
from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'preco',
            'descricao',
            'quantidade',
            'preco_compra',
            'preco_venda',
            'data_validade',
            'criado_em',
            'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
