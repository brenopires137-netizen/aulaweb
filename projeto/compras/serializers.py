from rest_framework import serializers
from .models import Compra


class CompraSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    fornecedor_nome = serializers.ReadOnlyField(source='fornecedor.nome_fantasia')

    class Meta:
        model = Compra
        fields = [
            'id',
            'produto',
            'produto_nome',
            'fornecedor',
            'fornecedor_nome',
            'preco',
            'data_compra',
            'quantidade',
            'criado_em',
        ]
        read_only_fields = ['id', 'criado_em']
