# Generated by Django 4.2.6 on 2024-03-12 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0004_product_max_people_product_min_people_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='available_products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hardqode.product', verbose_name='Доступные продукты'),
        ),
    ]
