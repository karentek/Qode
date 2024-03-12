from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


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
    created_by = models.OneToOneField(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Автор"
    )
    max_people = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="Максимум человек в группе",
        default=30
    )
    min_people = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="Минимум человек в группе",
        default=0
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Стоимость")

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
        max_length=20,
        verbose_name="Наименование группы"
    )
    students = models.ManyToManyField(
        Student,
        verbose_name="Студенты",
        blank=True
    )

    def __str__(self):
        return f"{self.pk} {self.name}"

