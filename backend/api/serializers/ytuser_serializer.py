from rest_framework import serializers
from videos_manager.models import YTUser


class YTUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTUser
        fields = '__all__'
