from students import views
from django.contrib import admin
from django.urls import path
from students.views import student_search_form,create_reverse,student_search_form
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('form/', views.handle_get_post, name='handle_get_post'),
    path('student/', views.create_reverse, name='student-search-form'),
    path('student/<str:student_id>/', views.student_search_form, name='show_inf'),
    ]

