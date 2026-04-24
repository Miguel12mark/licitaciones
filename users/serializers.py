from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 🔐 LOGIN CON EMAIL
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


# 👤 SERIALIZER DE USUARIO
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )