from django.db import migrations, models
import django.db.models.deletion

def set_default_duration(apps, schema_editor):
    Duration = apps.get_model('shop', 'Duration')
    default_duration1 = Duration.objects.create(name='Anual', slug='anual')
    Product = apps.get_model('shop', 'Product')
    for product in Product.objects.all():
        product.duration = default_duration1
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'duration',
                'verbose_name_plural': 'durations',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Duration', null=True),
        ),
        migrations.RunPython(set_default_duration),
        migrations.AlterField(
            model_name='product',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Duration'),
        ),
    ]