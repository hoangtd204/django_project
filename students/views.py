from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from students.crud_students.serializers import StudentSerializer
from .models import Student


class StudentCreate(APIView):
    error = None
    def post(self, request):
        student= request.data
        serializer = StudentSerializer(data=student)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'student/forms.html', {'success': 'Student registered successfully!'})
        else:

            error = "Student creation failed"
            return render(request, 'student/forms.html', {'error': error })
    def get(self, request):
        return render(request, 'student/forms.html')


def student_search_form(request):
    student = None
    error = None
    context = {}
    student_id = request.GET.get('student_id')
    if student_id:
        try:
            student = Student.objects.get(student_id=student_id)
            context['student'] = student
        except Student.DoesNotExist:
            error = "Student not found"

    return render(request, 'student/show_inf.html', {'student': student, 'error': error})
