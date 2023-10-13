from rest_framework import serializers

# Create your models here.
class QuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    video_id = serializers.IntegerField()
    time_stamp = serializers.CharField()
    question = serializers.CharField()
    answer = serializers.CharField()
    username = serializers.CharField()
