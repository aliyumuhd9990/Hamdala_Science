from django.db import models
from accounts.models import *
from student_app.models import Student, AcademicSession, Term
# Create your models here.


# USER_MODEL = User
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.session} - {self.term} - ₦{self.amount}"
    
class FeeStructure(models.Model):
    level = models.CharField(max_length=10, default=None)  # JS1, Primary 3, etc
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='fee_structures', default="None")
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.level} - {self.term} - ₦{self.amount}"