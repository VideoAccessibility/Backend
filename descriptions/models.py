from django.db import models

# Create your models here.
class Description(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_id = models.IntegerField()
    time_stamp_start = models.IntegerField()
    time_stamp_end = models.IntegerField()
    descriptions = models.CharField(max_length=300)
    modified_descriptions = models.CharField(max_length=10000, null=True)
    ai_or_human = models.CharField(max_length=100)
    group_id = models.CharField(max_length=100)
    group_star = models.IntegerField(default=0)
    username = models.CharField(max_length=200)
