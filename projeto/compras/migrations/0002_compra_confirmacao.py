from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='confirmada',
            field=models.BooleanField(default=False, verbose_name='Confirmada'),
        ),
        migrations.AddField(
            model_name='compra',
            name='confirmado_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Confirmado em'),
        ),
    ]
