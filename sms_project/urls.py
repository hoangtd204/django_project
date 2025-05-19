
from django.urls import path,include
from students.views import creat_student, student_search_form, student_update

urlpatterns = [
    path('form_create_student/', creat_student, name='form_create_student'),
    path('student_search/', student_search_form, name='student_search'),
    path('form_update_student/', student_update, name='form_update_student'),
    
]
