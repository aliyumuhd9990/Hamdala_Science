from django.shortcuts import render, redirect
from accounts.models import CustomUser
from django.db.models import Q
from django.contrib import messages

app_name = 'parent_app'


def search_parent(request):
    parents = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query')

        parents = CustomUser.objects.filter(
            Q(email__icontains=query) |
            Q(profile__contact__icontains=query)
        ).filter(role='parent')

        
    return render(request, 'parent/search_parent.html', {
        'parents': parents,
        'query': query
    })
    

def add_parent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        # 1️⃣ Check if user already exists
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # User exists but is not a parent
            if user.role != 'parent':
                messages.error(
                    request,
                    "This email already belongs to another staff account."
                )
                return redirect('parent_app:add_parent', parent_id=user.id)

            # Parent already exists
            if CustomUser.objects.filter(role='parent').exists():
                messages.info(
                    request,
                    "Parent already exists. You can now add student."
                )
                return redirect('student_app:add_student', parent_id=user.id)

        else:
            # 2️⃣ Create new user
            user = CustomUser.objects.create_user(
                email=email,
                password='parent123',
                role='parent',
                first_name=first_name,
                last_name=last_name
            )

        messages.success(request, "Parent added successfully.")
        return redirect('student_app:add_student', parent_id=user.id)

    return render(request, 'parent/add_parent.html')
