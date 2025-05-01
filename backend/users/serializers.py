from rest_framework import serializers
from users.models import CustomUser
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
    

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return False
    
    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    
class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ('avatar',)

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')
        if avatar is None:
            return serializers.ValidationError('Avatar is required.')
        
        instance.avatar = avatar
        instance.save()
        return instance
    