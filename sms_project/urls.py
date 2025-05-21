
from django.urls import path
from students.views import creat_student, search_student, update_student, delete_student

urlpatterns = [
      path('create/', creat_student),
      path('search/',search_student),
      path('update/<str:student_id>/', update_student),
      path('delete/<str:student_id>/', delete_student)
]
