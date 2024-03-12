from django.contrib import admin

from hardqode.models import Product, Group, Teacher, Student, Lesson


admin.site.register(Lesson)
admin.site.register(Product)
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Student)
