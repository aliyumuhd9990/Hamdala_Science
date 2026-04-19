from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import *
from student_app.models import Student, AcademicSession
from django.contrib.auth.decorators import login_required
from django.contrib import messages

NURSERY_LEVELS = [
    'pre_nursery','nursery_1','nursery_2',
]

PRIMARY_LEVELS = [
    'primary_1','primary_2','primary_3','primary_4','primary_5'
]

SECONDARY_LEVELS = [
    'jss_1','jss_2','jss_3',
    'sss_1','sss_2','sss_3'
]

ARMS = ['A','B','C']
    
@login_required
def principal_home(request):
    user = request.user
    arm = request.GET.get('arm') 

    current_session = AcademicSession.objects.filter(is_current=True).first()

    students = Student.objects.filter(session=current_session)
    current_session = AcademicSession.objects.filter(is_current=True).first()

    if user.role == 'p_principal':
        students = students.filter(level__in=PRIMARY_LEVELS)
        section = "Primary Section"

    elif user.role == 's_principal':
        students = students.filter(level__in=SECONDARY_LEVELS)
        section = "Secondary Section"
    elif user.role == 'n_principal':
        students = students.filter(level__in=NURSERY_LEVELS)
        section = "Nursery Section"

    else:
        section = "Unauthorized"

    context = {
        'section': section,
        'total_students': students.count(),
        'session': current_session,
        'students': students[:5],  # recent 5
        'arms': ARMS,
        'arm': arm,
        'classes': PRIMARY_LEVELS if user.role == 'p_principal' else SECONDARY_LEVELS if user.role == 's_principal' else NURSERY_LEVELS 
    }

    return render(request, 'principal/principal_home.html', context)

