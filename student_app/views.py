from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from student_app.models import *
from payment.models import *   # adjust if your app name differs
from django.db.models import Sum
from django.contrib import messages


NURSERY_LEVELS = [
    'pre_nursery', 'nursery_1','nursery_2',
]

PRIMARY_LEVELS = [
    'nursery_1','nursery_2',
    'primary_1','primary_2','primary_3','primary_4','primary_5'
]

SECONDARY_LEVELS = [
    'jss_1','jss_2','jss_3',
    'sss_1','sss_2','sss_3'
]

ARMS = ['A','B','C']

def generate_admission_number():
    last_student = Student.objects.order_by('created_at').last()

    if last_student:
        last_number = int(last_student.admission_number[3:])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"ADM{str(new_number).zfill(4)}"

def add_student(request, parent_id):
    parent = get_object_or_404(CustomUser, id=parent_id)

    session = AcademicSession.objects.filter(is_current=True).first()
    if not session:
        messages.error(request, "No active academic session.")
        return redirect('parent_app:search_parent')

    if request.method == 'POST':
        Student.objects.create(
            admission_number=generate_admission_number(),
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            level=request.POST['level'],
            arm=request.POST['arm'],
            parent=parent,
            session=session
        )

        messages.success(request, "Student added successfully.")
        return redirect('student_app:add_student', parent_id=parent_id)

    return render(request, 'student/add_student.html', {
        'parent': parent,
        'session': session
    })
    
def student_list(request):
    level = request.GET.get('level')
    arm = request.GET.get('arm')
    session_id = request.GET.get('session')
    term_id = request.GET.get('term')

    sessions = AcademicSession.objects.all().order_by('-name')

    if session_id:
        session = AcademicSession.objects.get(id=session_id)
    else:
        session = AcademicSession.objects.filter(is_current=True).first()

    students = Student.objects.filter(
        session=session,
        level=level,
        arm=arm
    )

    if term_id:
        students = students.filter(term_id=term_id)

    payments = Payment.objects.filter(student__in=students)

    # Create payment status dictionary
    payment_status = {
        payment.student_id: payment.amount for payment in payments
    }

    context = {
        'students': students,
        'sessions': sessions,
        'selected_session': session,
        'level': level,
        'arm': arm,
        'term_id': term_id,
        'payment_status': payment_status
    }

    return render(request, 'student/students_list.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    current_term = Term.objects.filter(
        session=student.session,
        is_current=True
    ).first()

    payments = Payment.objects.filter(
        student=student,
        session=student.session,
        term=current_term
    )

    total_paid = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # fee = FeeStructure.objects.get(
    #     level=student.level,
    #     term=current_term
    # ).first()

    school_fee = 20000
    balance = school_fee - total_paid

    context = {
        'student': student,
        'current_term': current_term,
        'payments': payments,
        'school_fee': school_fee,
        'total_paid': total_paid,
        'balance': balance,
    }

    return render(request, 'student/student_details.html', context)

def student_class(request):
    user = request.user
    arm = request.GET.get('arm') 

    current_session = AcademicSession.objects.filter(is_current=True).first()

    students = Student.objects.filter(session=current_session)
    current_session = AcademicSession.objects.filter(is_current=True).first()

    if user.role == 'n_principal':
        students = students.filter(level__in=NURSERY_LEVELS)
        section = "Nursery Section"

    elif user.role == 'p_principal':
        students = students.filter(level__in=PRIMARY_LEVELS)
        section = "Primary Section"
        
    elif user.role == 's_principal':
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
        'classes': NURSERY_LEVELS if user.role == 'n_principal' 
        else PRIMARY_LEVELS if user.role == 'p_principal'
        else SECONDARY_LEVELS
    }
    return render(request, 'student/student_class.html', context)