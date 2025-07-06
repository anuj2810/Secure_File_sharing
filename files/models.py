from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser

class UploadedFile(models.Model):
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
