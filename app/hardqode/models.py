from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Count
from django.utils import timezone


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
        verbose_name="Продукт",
        related_name='lessons'
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


def add_student_to_group_uniform_distribution(instance: Student, product: Product):
    """
    Добавляем студента в заранее подготовленные группы,
    сначала до тех пор, пока не достигнем минимально требуемого количества в группе,
    затем когда все группы минимально заполнены, добавляем равномерно по группам
    просто в наименьшую по количеству
    """
    min_people = product.min_people
    group_counts = Group.objects.filter(product=product).annotate(num_students=Count('students'))
    underfilled_groups = group_counts.filter(num_students__lt=min_people)
    underfilled_groups = underfilled_groups.order_by('-num_students')

    if underfilled_groups.exists():
        target_group = underfilled_groups.first()
    else:
        min_student_group = group_counts.order_by('num_students').first()
        target_group = min_student_group

    target_group.students.add(instance)


def add_student_to_group_non_uniform_distribution(instance: Student, product: Product):
    """
    Добавляем студента в группу пока не наберем максимальное количество, если
    группа переполнится, будет создана новая
    """
    groups = Group.objects.filter(product=product).prefetch_related('students')
    for group in groups:
        if group.students.count() < group.product.max_people:
            group.students.add(instance)
            return
    group_name = f"Группа на {product.description}"
    group = Group.objects.create(product=product, name=group_name)
    group.students.add(instance)


@receiver(m2m_changed, sender=Student.available_products.through)
def handle_student_product_change(instance: Student, action, pk_set, **kwargs):
    """
    Ловим сигнал добавления продукта к студенту и вызываем функцию
    в соответствии с выбранным в самом продукте алгоритмом распределения,
    если равномерный алгоритм распределения == True но продукт уже стартовал,
    распределение пройдет по обычному сценарию набора студентов
    """
    if action == "post_add":
        product = Product.objects.get(pk__in=pk_set)

        if product.uniform_distribution and timezone.now() < product.time_to_start:
            add_student_to_group_uniform_distribution(instance, product)
        else:
            add_student_to_group_non_uniform_distribution(instance, product)

