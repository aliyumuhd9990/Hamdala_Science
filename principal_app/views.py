from django.shortcuts import get_object_or_404, render, redirect
from parent_app.models import Parent
from student_app.models import Student, AcademicSession
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

PRIMARY_LEVELS = [
    'nursery_1','nursery_2',
    'primary_1','primary_2','primary_3','primary_4','primary_5'
]

SECONDARY_LEVELS = [
    'jss_1','jss_2','jss_3',
    'sss_1','sss_2','sss_3'
]

ARMS = ['A','B','C']

def add_student(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    

    session = AcademicSession.objects.filter(is_current=True).first()
    if not session:
        messages.error(request, "No active academic session.")
        return redirect('principal_app:principal_home')

    if request.method == 'POST':
        Student.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            level=request.POST['level'],
            arm=request.POST['arm'],
            parent=parent,
            session=session
        )

        messages.success(request, "Student added successfully.")
        return redirect('principal_app:principal_home')

    return render(request, 'principal/add_student.html', {
        'parent': parent
    })

@login_required
def principal_home(request):
    user = request.user
    arm = request.GET.get('arm') 

    current_session = AcademicSession.objects.filter(is_current=True).first()

    students = Student.objects.filter(session=current_session)
    current_session = AcademicSession.objects.filter(is_current=True).first()

    if user.role == 'primary_principal':
        students = students.filter(level__in=PRIMARY_LEVELS)
        section = "Primary Section"

    elif user.role == 'secondary_principal':
        students = students.filter(level__in=SECONDARY_LEVELS)
        section = "Secondary Section"

    else:
        section = "Unauthorized"

    context = {
        'section': section,
        'total_students': students.count(),
        'session': current_session,
        'students': students[:5],  # recent 5
        'arms': ARMS,
        'arm': arm,
        'classes': PRIMARY_LEVELS if user.role == 'primary_principal' else SECONDARY_LEVELS,
    }

    return render(request, 'principal/principal_home.html', context)

def search_parent(request):
    parents = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query')

        parents = Parent.objects.filter(
            Q(user__email__icontains=query) |
            Q(phone__icontains=query)
        )

        if not parents.exists():
            messages.warning(
                request,
                "Parent not found. Please add parent first."
            )

    return render(request, 'principal/search_parent.html', {
        'parents': parents,
        'query': query
    })