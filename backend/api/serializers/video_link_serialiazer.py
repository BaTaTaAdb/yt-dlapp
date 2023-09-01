from rest_framework import serializers


class VideoLinkSerializer(serializers.Serializer):
    link = serializers.URLField()
