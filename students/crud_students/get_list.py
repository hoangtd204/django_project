from students.crud_students.serializers import StudentSerializer
from students.models import Student


def find_student_by_id(student_id: str):
    student_id = student_id.strip()
    if not student_id:
        return None, None
    try:
        student = Student.objects.get(student_id=student_id)
        student = StudentSerializer(student).data
        return student, None
    except Student.DoesNotExist:
        return None , None
