from rest_framework import serializers

from .models import Venda


class VendaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.ReadOnlyField(source='cliente.nome')
    produto_nome = serializers.ReadOnlyField(source='produto.nome')

    class Meta:
        model = Venda
        fields = [
            'id',
            'cliente',
            'cliente_nome',
            'produto',
            'produto_nome',
            'preco_unitario',
            'data_venda',
            'quantidade',
            'confirmada',
            'confirmado_em',
            'criado_em',
        ]
        read_only_fields = ['id', 'confirmado_em', 'criado_em']
