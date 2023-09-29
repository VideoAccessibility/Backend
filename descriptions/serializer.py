from rest_framework import serializers

class DescriptionsSerializer(serializers.Serializer):
    id = models.CharField()
    created_at = models.DateTimeField()
    video_id = models.IntegerField()
    time_stamp = models.CharField()
    descriptions = models.CharField()
    modified_descriptions = models.CharField()
    ai_or_human = models.CharField()
    group_id = models.CharField()
    group_star = models.IntegerField()
    username = models.CharField()
