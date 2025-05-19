
from django.shortcuts import render
from django.template.response import TemplateResponse
from students.crud_students.search_student_byid import find_student_by_id
from students.crud_students.create_student import save_student
from students.crud_students.update_student import  change_student_inf


def creat_student(request):
    if request.method == 'POST':
        student = {
            'student_id': request.POST.get('student_id'),
            'name': request.POST.get('name'),
            'age': request.POST.get('age'),
            'major': request.POST.get('major'),
        }
        result = save_student(student)
        if result:
            return render(request, 'student/form_create_student.html', {
                'success': 'Student registered successfully!'
            })
        else:
            return render(request, 'student/form_create_student.html', {
                'error': 'Student creation failed'
            })
    else:
        return render(request, 'student/form_create_student.html')


# search_student_by_sid
def student_search_form(request):
    student_id_for_searching = request.GET.get('student_id', '')
    student, error = find_student_by_id(student_id_for_searching)
    context = {
        'student': student,
        'error_for_searching': error
    }
    return TemplateResponse(request, 'student/show_inf.html', context)




def student_update(request):
    if request.method == 'GET':
        student_id_for_updating = request.GET.get('student_id', '')
        student, error = find_student_by_id(student_id_for_updating)
        context = {
            'student': student,
            'error_for_update': error
        }
        return TemplateResponse(request, 'student/form_update_student.html', context)
    else :
        return render(request, 'student/form_update_student.html')