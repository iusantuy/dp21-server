from rest_framework import serializers
from django.contrib.auth import authenticate
from ..infrastructure.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "full_name"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user:
            raise serializers.ValidationError("Username atau password salah.")
        if not user.is_active:
            raise serializers.ValidationError("Akun dinonaktifkan.")
        data["user"] = user
        return data


# from django.contrib.auth import authenticate
# user = authenticate(username="admin", password="admin")
# print(user)  # harus muncul objek user, bukan None













# # users/presentation/serializers.py
# from rest_framework import serializers
# from user.infrastructure.models import CustomUser
# from django.contrib.auth import authenticate

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ["email", "name", "password"]

#     def create(self, validated_data):
#         return CustomUser.objects.create_user(**validated_data)

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if not user:
#             raise serializers.ValidationError("Invalid email or password")
#         return user

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ["id", "email", "name"]
