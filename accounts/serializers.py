from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from .models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'sacconame']  # sacconame is now required for normal users

    def validate(self, attrs):
        request = self.context.get('request')
        is_superuser = False

        if request and request.user and request.user.is_authenticated:
            is_superuser = request.user.is_superuser

        # Enforce sacco only if not a superuser
        if not is_superuser and not attrs.get('sacconame'):
            raise serializers.ValidationError("You must choose a Sacco to register.")

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'firstname', 'lastname',
            'avatar', 'role',
            'date_joined', 'is_active', 'is_staff'
        ]
        read_only_fields = fields


class MyTokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        if user.avatar:
            token['avatar_url'] = user.avatar.url if hasattr(user.avatar, 'url') else str(user.avatar)
        return token


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})