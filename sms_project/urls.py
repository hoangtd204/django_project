from students import views
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from students.views import StudentCreate, student_search_form

urlpatterns = [
    path('form_create_student/', StudentCreate.as_view(), name='form_create_student'),
    path('student_search/', student_search_form, name='student_search'),
]
