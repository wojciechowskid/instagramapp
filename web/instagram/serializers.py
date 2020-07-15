from rest_framework import serializers
from .models import InstagramAccount


class AuthCodeSerializer(serializers.Serializer):
    auth_code = serializers.CharField(max_length=255)


class InstagramAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = ['user', 'inst_user_id', 'long_lived_token', 'expires_in']
