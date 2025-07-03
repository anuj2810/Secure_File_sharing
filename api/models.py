from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):


    # 🔸 Custom user type field
    USER_TYPE_CHOICES = (
        ('ops', 'Operations User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # 🔸 Email verification flag
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.user_type})"



User = get_user_model()

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
