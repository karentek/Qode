# Generated by Django 4.2.6 on 2024-03-12 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0005_alter_student_available_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='hardqode.teacher', verbose_name='Автор'),
        ),
    ]
