from rest_framework import serializers

class DescriptionsSerializer(serializers.Serializer):
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    video_id = serializers.IntegerField()
    time_stamp = serializers.CharField()
    descriptions = serializers.CharField()
    modified_descriptions = serializers.CharField()
    ai_or_human = serializers.CharField()
    group_id = serializers.CharField()
    group_star = serializers.IntegerField()
    username = serializers.CharField()