from django.db import models
from accounts.models import CustomUser
from accounts.models import TimeStampedModel
from django.urls import reverse
import uuid


LEVEL_CHOICES = (
    ('nursery_1', 'Nursery 1'),
    ('nursery_2', 'Nursery 2'),
    ('primary_1', 'Primary 1'),
    ('primary_2', 'Primary 2'),
    ('primary_3', 'Primary 3'),
    ('primary_4', 'Primary 4'),
    ('primary_5', 'Primary 5'),
    ('jss_1', 'JSS 1'),
    ('jss_2', 'JSS 2'),
    ('jss_3', 'JSS 3'),
    ('sss_1', 'SSS 1'),
    ('sss_2', 'SSS 2'),
    ('sss_3', 'SSS 3'),
)

ARM_CHOICES = (('A','A'),('B','B'),('C','C'))

class AcademicSession(models.Model):
    name = models.CharField(max_length=20)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Term(models.Model):
    TERM_CHOICES = [
        ('first', 'First Term'),
        ('second', 'Second Term'),
        ('third', 'Third Term'),
    ]

    name = models.CharField(max_length=10, choices=TERM_CHOICES)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_name_display()} - {self.session.name}"
class Student(TimeStampedModel):
    admission_number = models.CharField(max_length=20, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    arm = models.CharField(max_length=1, choices=ARM_CHOICES)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    # term = models.ForeignKey(Term, on_delete=models.CASCADE, default=Term.objects.filter(is_current=True).first())
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.admission_number + ")"

    def save(self, *args, **kwargs):
        if not self.admission_number:
            self.admission_number = f"STD{Student.objects.count()+1:05d}"
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'id': self.id})
        
