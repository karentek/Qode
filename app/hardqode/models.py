import math

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import F, Count


class Teacher(models.Model):
    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя"
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Фамилия"
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    description = models.CharField(
        max_length=100,
        verbose_name="Описание"
    )
    time_to_start = models.DateTimeField(
        verbose_name="Дата старта обучения"
    )
    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Автор"
    )
    max_people = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        verbose_name="Максимум человек в группе",
        default=3
    )
    min_people = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        verbose_name="Минимум человек в группе",
        default=0
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Стоимость")

    uniform_distribution = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.pk} - {self.description}"


class Student(models.Model):
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя"
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Фамилия"
    )
    available_products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="Доступные продукты",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Lesson(models.Model):

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    description = models.CharField(
        max_length=150,
        verbose_name="Тема"
    )
    link = models.CharField(
        max_length=150,
        verbose_name="Ссылка на видео"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Продукт"
    )

    def __str__(self):
        return f"{self.pk} {self.description}"


class Group(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование группы"
    )
    students = models.ManyToManyField(
        Student,
        verbose_name="Студенты",
        blank=True
    )

    def __str__(self):
        return f"{self.pk} {self.name}"


@receiver(m2m_changed, sender=Student.available_products.through)
def add_student_to_group(instance: Student, action, pk_set, **kwargs):
    if action == "post_add":

        product = Product.objects.get(pk__in=pk_set)
        if product.uniform_distribution:
            groups = Group.objects.filter(product=product).annotate(num_students=Count('students'))
            target_group = groups.order_by('num_students').first()
            target_group.students.add(instance)
        else:
            groups = Group.objects.filter(product=product).prefetch_related('students')
            for group in groups:
                if group.students.count() < group.product.max_people:
                    group.students.add(instance)
                    break
            else:
                group_name = f"Группа на {product.description}"
                group = Group.objects.create(product=product, name=group_name)
                group.students.add(instance)

