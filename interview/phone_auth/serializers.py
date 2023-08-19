from rest_framework import serializers
from .models import CustomUser, InviteCode


class UserProfileSerializer(serializers.ModelSerializer):
    invite_code_code = serializers.SerializerMethodField()
    activation_code_code = serializers.SerializerMethodField()
    invited_users = serializers.SerializerMethodField ()

    def get_invite_code_code(self, obj):
        return obj.invite_code.invite_code if obj.invite_code else None
    
    def get_activation_code_code(self, obj):
        return obj.activation_code.invite_code if obj.activation_code else None
    
    def get_invited_users(self, obj):
        return [user.username for user in obj.invite_code.users_activated.all()] if obj.invite_code else None

    class Meta:
        model = CustomUser
        fields = ['username', 'invite_code_code', 'activation_code_code', 'invited_users']


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class PhoneCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    phone_code = serializers.CharField(max_length=4)

class ActivateCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)