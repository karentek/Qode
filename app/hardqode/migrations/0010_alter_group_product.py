# Generated by Django 4.2.6 on 2024-03-12 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0009_alter_lesson_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardqode.product', verbose_name='Продукт'),
        ),
    ]
