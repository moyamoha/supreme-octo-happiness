from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Todo, User
from django.contrib.auth.password_validation import validate_password


class UserAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["password1", "password2", "email", "first_name", "last_name"]

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        first_name = ""
        if 'first_name' in validated_data:
            first_name = validated_data['first_name']
        last_name = ""
        if 'last_name' in validated_data:
            last_name = validated_data['last_name']
        user = User.objects.create(
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ["id", "name", "description", "created", "status"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(
        required=True, validators=[validate_password])
    new_password = serializers.CharField(
        required=True, validators=[validate_password])

    def validate_new_password(self, value):
        validate_password(value)
        return value
