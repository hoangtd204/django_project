from students.crud_students.serializers import Student
from django.forms.models import model_to_dict
from students.crud_students.serializers import StudentSerializer
from rest_framework.response import Response


def find_student_by_id_for_update(student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        return True, student
    except Student.DoesNotExist:
        return False, None


def change_student_inf(request, student):
    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return True, serializer.data
    return False, serializer.errors
