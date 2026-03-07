from django.urls import path
from principal_app.views import *
from .views import *

app_name = "student_app"
 
urlpatterns = [
    path('add_student/<uuid:parent_id>/', add_student, name='add_student'),
    path('student_list/', student_list, name='student_list'),
    path('student_class/', student_class, name='student_class'),
    path('details/<uuid:student_id>/', student_detail, name='student_detail'),
]
