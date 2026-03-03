from django.urls import path
from principal_app.views import add_student
from .views import *

app_name = "student_app"
 
urlpatterns = [
    path('add-student/', add_student, name='add_student'),
    path('student_list/', student_list, name='student_list'),
    path('details/<int:student_id>/', student_detail, name='student_detail'),
]
