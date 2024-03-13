from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls)),
]