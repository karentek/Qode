from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lesson, Student, Product
from .serializers import LessonSerializer, ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    http://127.0.0.1:8000/api/lessons/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ViewSet):
    """
    example get request
    http://127.0.0.1:8000/api/lessons/available_lessons/?student_id=2
    """
    @action(detail=False)
    def available_lessons(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=400)

        try:
            student = Student.objects.prefetch_related('available_products').get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        product = student.available_products.first()
        if not product:
            return Response({'error': 'Student has no available products'}, status=400)

        lessons = Lesson.objects.filter(product=product).select_related('product')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
