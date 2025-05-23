
from django.urls import path
from students.views import creat_student, search_student, update_student, delete_student,student_list

urlpatterns = [
      path('create/', creat_student),
      path('search/',search_student),
      path('students/',student_list),
      path('update/<str:student_id>/', update_student),
      path('delete/<str:student_id>/', delete_student)
]
