from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

app_name = "student_app"
# Create your views here.
def AddStudent(request):
    if request.method == "POST":
        parent_email = request.POST['email']
        stu_name = request.POST['stu_name']
        stu_section = request.POST['stu_section']
        stu_class = request.POST['stu_class']
        stu_grade = request.POST['stu_grade']

        student, created = Student.objects.get_or_create(
                stu_parent=parent_email,
                stu_name=stu_name,
                stu_section=stu_section,
                stu_class=stu_class, 
                stu_grade=stu_grade, 
            )
        student.save()
        messages.SUCCESS(request, 'Student Added Successful!')
        return redirect('student_app:add_student')
    return render(request, 'student/add_student.html')

def StudentList(request):
    return render(request, 'student/student_list.html')
def StudentDetails(request):
    return render(request, 'student/student_details.html')

