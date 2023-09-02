from django.db import models

# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_id = models.IntegerField()
    time_stamp = models.CharField(max_length=200)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
    username = models.CharField(max_length=200)
 