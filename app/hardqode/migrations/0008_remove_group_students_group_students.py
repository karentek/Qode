# Generated by Django 4.2.6 on 2024-03-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardqode', '0007_remove_student_available_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='students',
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(to='hardqode.student', verbose_name='Студенты'),
        ),
    ]
