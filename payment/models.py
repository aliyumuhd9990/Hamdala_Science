from django.db import models
from accounts.models import *
from student_app.models import Student, AcademicSession
# Create your models here.

# USER_MODEL = User
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)