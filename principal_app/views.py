from django.shortcuts import render, redirect

app_name = 'principal_app'
# Create your views here.
def PrincipalDash(request):
    classes = [
        "One", "Two", "Three", "Four", "Five",
        "Six", 
    ]
    context = {
        "classes": classes,
    }
    return render(request, 'principal/principal_home.html', context)
def PrincipalProfile(request):
    return render(request, 'principal/user-profile.html')