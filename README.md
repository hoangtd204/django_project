#comment demo
Sử dụng SQLite3 khởi tạo 1 table chứa thông của 8 student  field including student_id,name,age,major
urls.py sẽ có 2 path là:
  path('student/', views.create_reverse, name='student-search-form'),
  path('student/<str:student_id>/', views.student_search_form, name='show_inf')

views.py sẽ có 2 def:

#client rrequest method get đến " http://127.0.0.1:8000/student/ "   sẽ render ra student_search.html và nếu người dùng post student_id sẽ tạo ra 1 url mới dựa tên student_id vừa post và 
redirect đến 'student/<str:student_id>/ ví dụ http://127.0.0.1:/student/PH34567/

def create_reverse(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            url = reverse('show_inf', kwargs={'student_id': student_id})
            return redirect(url)
    return render(request, 'students/student_search.html')
  


#khi client request method get đến http://127.0.0.1:/student/PH34567/ sẽ kiển tra PH34567 có tồn tại trong DB hay không và sẽ render ra show_inf.html

def student_search_form(request, student_id):
    context = {}
    try:
        student = Student.objects.get(student_id=student_id)
        context['student'] = student
    except Student.DoesNotExist:
        context['error'] = "Student not found"
    return render(request, 'students/show_inf.html', context)
    
