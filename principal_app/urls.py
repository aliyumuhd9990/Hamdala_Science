from django.urls import path
from .views import *

app_name = 'principal_app'

urlpatterns = [
    path('principal-dashboard/', principal_home, name='principal_home'),
]