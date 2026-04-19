from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import views as auth_views


# from allauth.account.views import 
#activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import *

# Create your views here.
#pyhton manage.py migrate --run-syncdb
def SignupView(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if password1 != password2:
            messages.error(request, "Password Don't Match!!")
            return redirect('signup')

        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exist!!')
            return redirect(reverse('signup'))
        else:
            user = CustomUser.objects.create_user(
                first_name=fname,
                last_name=lname,
                email=email,
                password=password1
            )

            # ✅ No need to manually create Profile, signal handles it.

            # 🔐 User activation email
            current_site = get_current_site(request)
            mail_subject = 'Your account needs to be verified'
            context = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user),
            }
            message = render_to_string('accounts/email_verified.html', context)
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email=' + email)

    return render(request, 'accounts/sign-up.html')

def ActivateEmailView(request, token, uidb64):
        try:
             uid = urlsafe_base64_decode(uidb64).decode()
             user = CustomUser._default_manager.get(id=uid) 
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
             user = None

        if user is not None and default_token_generator.check_token(user, token):
             user.is_active = True
             user.save()
             messages.success(request, 'Congratulations! Your account is activated!')
             return redirect(reverse('login'))
        else:
             messages.error(request, 'Invalid Activation Link!')
             return redirect(reverse('signup'))
             
             
        # return HttpResponse("Account Activated!")
def SentEmailView(request):
     return render(request, 'accounts/email_sent.html')


def LoginView(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']   # selected role from form

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # 🔹 Check role condition
            if user.role != role:
                messages.error(request, "You are not allowed to log in as this role.")
                return redirect('login')
            if user.role == "parent":
                auth.login(request, user)
                return redirect(reverse('core_app:index'))
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('login')
    else:
        return render(request, 'accounts/sign-in.html')
def StaffLoginView(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # selected role from form

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # 🔹 Check role condition
            if user.role == "parent":
                messages.error(request, "You are not allowed to log in as this role.")
                return redirect('staff_login')
            if user.role == "s_principal":
                auth.login(request, user)
                return redirect(reverse('principal_app:principal_home'))
            elif user.role == "p_principal":
                auth.login(request, user)
                return redirect(reverse('principal_app:principal_home'))
            elif user.role == "n_principal":
                auth.login(request, user)
                return redirect(reverse('principal_app:principal_home'))
            elif user.role == "accountant":
                pass
            elif user.role == "manager":
                pass
            elif user.role == "teacher":
                pass
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('staff_login')
    else:
        return render(request, 'accounts/staff-login.html')

@login_required
def AccountView(request):
     user = request.user
     profile, created = Profile.objects.get_or_create(user=user)

     context = {
          'user' : user,
          'profile': profile,
     }
     return render(request, 'accounts/account.html', context)


@login_required
def EditProfileView(request):
     user = request.user
     profile = Profile.objects.get(user=request.user)

     context = {
        'user': user,
        'profile': profile, 
     }
     

     if not profile.profile_img:
          profile.profile_img = 'img/profile.png'

     if request.method == "POST":
          #this is for the CustomUser table
          user.first_name = request.POST.get('fname', user.first_name)#updating new name
          user.last_name = request.POST.get('lname', user.last_name)#updating new name
          user.email = request.POST.get('email', user.email)#updating new email

          #this is for profile table
          profile.contact = request.POST.get('contact', profile.contact)
          profile.bio = request.POST.get('bio', profile.bio)
        #   img = request.FILES.get('file')
          

          if request.FILES.get('file'):
               profile.profile_img = request.FILES['file']



          user.save()
          profile.save()
          messages.success(request, 'Profile Updated!!')
        
          return redirect(reverse('account'))
     return render(request, 'accounts/edit-profile.html', context)

def VerifyView(request):
    return render(request, 'accounts/email_verification.html')


@login_required
def logoutView(request):
    user = request.user
    if user is not None:
            if user.role == "s_principal":
                auth.logout(request)
                return redirect('staff_login')
            elif user.role == "p_principal":
                auth.logout(request)
                return redirect('staff_login')
            elif user.role == "accountant":
                pass
            elif user.role == "manager":
                pass
            elif user.role == "teacher":
                pass
    auth.logout(request)
    return redirect(reverse('login'))
