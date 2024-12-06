# Generated by Django 4.2.7 on 2024-12-04 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirección', models.CharField(max_length=255)),
                ('código_postal', models.IntegerField(max_length=5)),
                ('ciudad', models.CharField(max_length=50)),
                ('método_pago', models.CharField(choices=[('CR', 'Contrareembolso'), ('TJ', 'Tarjeta')], default='TJ', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
