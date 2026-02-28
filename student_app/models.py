from django.db import models
from accounts.models import CustomUser

# Create your models here.
STUDENT_CLASS = (
    ('nus1', 'Nursery 1'),
    ('nus2', 'Nursery 2'),
    ('prm1', 'Primary 1'),
    ('prm2', 'Primary 2'),
    ('prm3', 'Primary 3'),
    ('prm4', 'Primary 4'),
    ('prm5', 'Primary 5'),
    ('jss1', 'JSS 1'),
    ('jss2', 'JSS 2'),
    ('jss3', 'JSS 3'),
    ('sss1', 'SSS 1'),
    ('sss2', 'SSS 2'),
    ('sss3', 'SSS 3'),   
)

SECTION = (
    ('prm_sec', 'Primary Section'),
    ('sec_sec', 'Secondary Section'),
)

CLASS_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)
class Student(models.Model):
    stu_parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_parent')
    stu_name = models.CharField(max_length=100)
    stu_section = models.CharField(max_length=100, choices=SECTION, default="None", null=False, blank=False)
    stu_class = models.CharField(max_length=100, choices=STUDENT_CLASS, default="None", null=False, blank=False)
    stu_grade = models.CharField(max_length=100, choices=CLASS_GRADE, default="A", null=False, blank=False)
    stu_img = models.ImageField(upload_to='img_root/',  blank=True, null=False)
    on_scholership = models.BooleanField(default=False)
    
    def __str__(self):
        return self.stu_name