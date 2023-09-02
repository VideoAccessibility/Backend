from rest_framework import serializers

# Create your models here.
class QuestionSerializer(serializers.Serializer):
    id = models.CharField()
    created_at = models.DateTimeField()
    video_id = models.IntegerField()
    time_stamp = models.CharField()
    question = models.CharField()
    answer = models.CharField()
    username = models.CharField()
