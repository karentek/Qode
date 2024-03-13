# Generated by Django 4.2.6 on 2024-03-13 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0013_alter_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_people',
            field=models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Максимум человек в группе'),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_people',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)], verbose_name='Минимум человек в группе'),
        ),
    ]