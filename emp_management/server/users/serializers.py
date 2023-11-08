from rest_framework import serializers

from employee.models import Employee
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password2",
            "type",
            "department",
            "last_name",
            "first_name",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        if validated_data.get("type") == "EMP":
            permissions = Group.objects.get(name="Employee").id

        elif validated_data.get("type") == "HR":
            permissions = Group.objects.get(name="HR").id

        elif validated_data.get("type") == "OW":
            permissions = Group.objects.get(name="Owner").id

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["email"],
            type="EMP",
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.groups.add(permissions)
        employee = Employee.objects.create(
            user=user, department=validated_data.get("department", "")
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid email or password.')
