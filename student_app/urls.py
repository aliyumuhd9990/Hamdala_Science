from django.urls import path
from .views import *

app_name = "student_app"
 
urlpatterns = [
    path('add_student/', AddStudent, name='add_student'),
    path('student_list/', StudentList, name='student_list'),
    path('student_details/', StudentDetails, name='student_details')
]
