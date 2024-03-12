# Generated by Django 4.2.6 on 2024-03-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0006_alter_product_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='available_products',
        ),
        migrations.AddField(
            model_name='student',
            name='available_products',
            field=models.ManyToManyField(blank=True, to='hardqode.product', verbose_name='Доступные продукты'),
        ),
    ]