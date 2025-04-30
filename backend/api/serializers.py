from rest_framework import serializers
from users.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')

    def validate_first_name(self, value):
        if not value:
            return serializers.ValidationError('Обязательное поле.')
        return value
    
    def validate_last_name(self, value):
        if not value:
            return serializers.ValidationError('Обязательное поле.')
        return value
    
class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return False