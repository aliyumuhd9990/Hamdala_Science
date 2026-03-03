from django.urls import path
from .views import *

app_name = 'principal_app'

urlpatterns = [
    path('add_student/<int:parent_id>/', add_student, name='add_student'),
    path('principal-dashboard/', principal_home, name='principal_home'),
    path('search-parent/', search_parent, name='search_parent'),
]