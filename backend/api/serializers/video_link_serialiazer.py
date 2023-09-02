from rest_framework import serializers
from django.contrib.auth.models import User


class VideoLinkSerializer(serializers.Serializer):
    link = serializers.URLField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
