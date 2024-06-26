from rest_framework import serializers

class VideosSerializer(serializers.Serializer):
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    video_path = serializers.CharField()
    url = serializers.CharField()
    public_or_private = serializers.CharField()