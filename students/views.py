from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student


def index(request):
    return render(request, 'students/index.html')

def handle_get_post(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return HttpResponse(f"You just have send with a name: {name}")
    else:
        name = request.GET.get('name', '')
        return render(request, 'students/forms.html', {'name': name})





def student_search_form(request, student_id):
    context = {}
    try:
        student = Student.objects.get(student_id=student_id)
        context['student'] = student
    except Student.DoesNotExist:
        context['error'] = "Student not found"

    return render(request, 'students/show_inf.html', context)

def create_reverse(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            url = reverse('show_inf', kwargs={'student_id': student_id})
            return redirect(url)
    return render(request, 'students/student_search.html')
