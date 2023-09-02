from django.db import models

# Create your models here.
class Description(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_id = models.IntegerField()
    time_stamp = models.CharField(max_length=200)
    descriptions = models.CharField(max_length=300)
    modified_descriptions = models.CharField(max_length=10000, null=True)
    username = models.CharField(max_length=200)
