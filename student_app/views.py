from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from student_app.models import Student, AcademicSession
from payment.models import Payment   # adjust if your app name differs
from django.db.models import Sum


PRIMARY_LEVELS = [
    'nursery_1','nursery_2',
    'primary_1','primary_2','primary_3','primary_4','primary_5'
]

SECONDARY_LEVELS = [
    'jss_1','jss_2','jss_3',
    'sss_1','sss_2','sss_3'
]

def student_list(request):
    level = request.GET.get('level')   # js1, ss1 etc
    arm = request.GET.get('arm')       # A, B, C
    session_id = request.GET.get('session')

    sessions = AcademicSession.objects.all().order_by('-name')

    if session_id:
        session = AcademicSession.objects.get(id=session_id)
    else:
        session = AcademicSession.objects.filter(is_current=True).first()

    # ✅ STRICT FILTERING
    students = Student.objects.filter(
        session=session,
        level=level,
        arm=arm
    )

    context = {
        'students': students,
        'sessions': sessions,
        'selected_session': session,
        'level': level,
        'arm': arm,
    }
    return render(request, 'student/students_list.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    payments = Payment.objects.filter(
        student=student,
        session=student.session
    )

    total_paid = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # TEMPORARY SCHOOL FEE
    school_fee = 50000  

    balance = school_fee - total_paid

    context = {
        'student': student,
        'payments': payments,
        'total_paid': total_paid,
        'school_fee': school_fee,
        'balance': balance,
    }

    return render(request, 'student/student_details.html', context)