from django.db import models

# Create your models here.
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    video_path = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200)
    public_or_private = models.CharField(max_length=200)
