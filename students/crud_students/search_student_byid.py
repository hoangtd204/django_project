
from django.forms.models import model_to_dict
from students.models import Student

def find_student_by_id(student_id: str):
    student_id = student_id.strip()
    if not student_id:
        return None, None
    try:
        student = Student.objects.get(student_id=student_id)
        student_dict = model_to_dict(student)
        return student_dict, None
    except Student.DoesNotExist:
        return None, "Student not found."
