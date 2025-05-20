from students.crud_students.serializers import Student, StudentSerializer
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError, ObjectDoesNotExist

def convert_json_to_dict(request):
    student = {
        'student_id': request.POST.get('student_id'),
        'name': request.POST.get('name'),
        'age': request.POST.get('age'),
        'major': request.POST.get('major'),
    }
    return student

def find_student_by_id_for_update(student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        return model_to_dict(student)
    except Student.DoesNotExist:
        return "Student not found."




def change_student_inf(student_target, data_for_update):
    try:
        student = Student.objects.get(id=student_target)
    except ObjectDoesNotExist:
        return False, "Student not exist "

    for key, value in data_for_update.items():
        setattr(student, key, value)

    try:
        student.full_clean()
    except ValidationError as e:
        return False, "Update failed"
    student.save()
    return True, "Updated Successfully!"

