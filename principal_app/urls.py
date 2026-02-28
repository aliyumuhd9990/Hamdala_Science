from django.urls import path
from .views import *

app_name = 'principal_app'

urlpatterns = [
    path('principal_dash/', PrincipalDash, name='principal_home'),
    path('profile/', PrincipalProfile, name='principal_profile')
]
