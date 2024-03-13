# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from models import Student, Product, Group
#
#
# @receiver(m2m_changed, sender=Student.available_products.through)
# def add_student_to_group(sender, instance, action, reverse, model, pk_set, **kwargs):
#     print("* " * 50)
#
#     if action == "post_add":
#         # Get the product added to the student
#         product = Product.objects.get(pk__in=pk_set)
#
#         # Get all groups related to the added product
#         groups = Group.objects.filter(product=product)
#
#         # Iterate through each group
#         for group in groups:
#             # Check if the group has space for more students
#             if group.students.count() < group.product.max_people:
#                 # Add the student to the group
#                 group.students.add(instance)
#                 break  # Stop after adding to the first eligible group
#         else:
#             # If no group has space, create a new group
#             group_name = f"Group for {product.description}"
#             group = Group.objects.create(product=product, name=group_name)
#             group.students.add(instance)
