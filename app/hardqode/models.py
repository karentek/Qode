from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    description = models.CharField(max_length=100)
    time_to_start = models.DateTimeField()
    created_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    min_count_of_members = models.SmallIntegerField()
    max_count_of_members = models.SmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Student(models.Model):
    name = models.CharField(max_length=100)
    available_products = models.ForeignKey(Product, on_delete=models.CASCADE)


class Lesson(models.Model):
    description = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    product = models.OneToOneField(Product, on_delete=models.PROTECT)


class Group(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)

