from rest_framework import serializers
from .models import Product, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'description', 'link']


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'description', 'time_to_start', 'max_people', 'min_people', 'price', 'lessons']