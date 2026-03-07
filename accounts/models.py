from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import uuid
from django.urls import reverse
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    ROLE_CHOICES = (
        ('parent', 'parent'),
        ('teacher', 'teacher'),
        ('e_officer', 'exam efficer'),
        ('manager', 'manager'),
        ('s_principal', 'secondary principal'),
        ('p_principal', 'primary principal'),
        ('accountant', 'accountant'),
    )

    first_name = models.CharField(max_length=30, blank=False, default="None")
    last_name = models.CharField(max_length=30, blank=False, default="None")
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Django’s built-in "staff" flag
    date_joined = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"id": self.id})
    

    def __str__(self):
        return f"{self.email} ({self.role})"


class Profile(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    email_token = models.CharField(max_length=200, default=False)
    is_verified = models.BooleanField(default=False)
    contact = models.CharField(max_length=11, default="080xxxxxx")
    bio = models.TextField(default="I'm New Here...............")
    profile_img = models.ImageField(upload_to='img_root/',  blank=True, null=False)

    def __self__(self):
        return self.user.email

