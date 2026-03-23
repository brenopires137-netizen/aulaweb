from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_remove_compra_prazo_validade_dias'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compra',
            old_name='preco',
            new_name='preco_compra',
        ),
        migrations.AddField(
            model_name='compra',
            name='preco_venda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Preco de venda'),
            preserve_default=False,
        ),
        migrations.RunSQL(
            sql='UPDATE compras_compra SET preco_venda = preco_compra',
            reverse_sql='UPDATE compras_compra SET preco_venda = 0',
        ),
        migrations.AlterField(
            model_name='compra',
            name='preco_compra',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preco de compra'),
        ),
    ]
