
from django.shortcuts import render
from django.template.response import TemplateResponse
from students.crud_students.search_student_byid import find_student_by_id
from students.crud_students.create_student import save_student
from students.crud_students.update_student import  change_student_inf,convert_json_to_dict,find_student_by_id_for_update


def creat_student(request):
    if request.method == 'POST':
        student = convert_json_to_dict(request)
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
        'error_for_search': error
    }
    return TemplateResponse(request, 'student/show_inf.html', context)


#update_student's inf
def student_update(request):
    if request.method == 'POST':
        student_id_for_updating = request.POST.get('student_id', '')
        form_type = request.POST.get('form_type')
        if form_type == 'form1':
            student, error = find_student_by_id(student_id_for_updating)
            context = {
                'student': student,
                'error_for_updating': error
            }
            return TemplateResponse(request, 'student/form_update_student.html', context)
        else:
            # student_id_from form1
            student_id = request.POST.get('student_id_for_update')
            student_target = find_student_by_id_for_update(student_id)
            id_of_student_target = student_target.get('id')
            #get student from post request
            student_for_updating  = convert_json_to_dict(request)
            updated, error = change_student_inf(id_of_student_target, student_for_updating)
            context = {
                'error_for_updating': error,
            }

            if updated:
                return TemplateResponse(request, 'student/form_update_student.html', context)
            else:

                return TemplateResponse(request, 'student/form_update_student.html', context)
    else:
        return TemplateResponse(request, 'student/form_update_student.html')
