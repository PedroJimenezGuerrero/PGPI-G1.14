# Generated by Django 4.2.7 on 2024-12-04 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_fecha_inicio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'categorias', 'verbose_name_plural': 'categorias'},
        ),
        migrations.AlterModelOptions(
            name='duration',
            options={'ordering': ('name',), 'verbose_name': 'duraciones', 'verbose_name_plural': 'duraciones'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'productos', 'verbose_name_plural': 'productos'},
        ),
    ]
