# accounts/serializers.py

from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    
    password1 = serializers.CharField(
        write_only=True)  # Adding confirm password
    password2 = serializers.CharField(
        write_only=True)  # Adding confirm password

    class Meta:
        # model = CustomUser
        model = get_user_model()
        # REQUIRED FIELDS
        fields = ['id', 'fullname', 'national_code', 'email', 'department', 'student_number', 'password1', 'password2']
        read_only_fields = []  # Fields that should not be editable

        extra_kwargs = {
            # 'password': {'write_only': True},  # Password should be write-only
            # 'confirm_password': {'write_only': True}  # Confirm password should also be write-only
        }

    def validate(self, data):
        """
        Validate password and confirm_password if provided.
        """
        # print('data', data)
        password = data.get('password1')
        confirm_password = data.get('password2')

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a user with the validated data.
        """
        password = validated_data.pop('password1')
        validated_data.pop('password2')  # Remove confirm password field

        # Create the user
        user = CustomUser.objects.create(
            fullname=validated_data.get('fullname'),
            national_code=validated_data.get('national_code'),
            email=validated_data.get('email'),
            department=validated_data.get('department'),
            student_number=validated_data.get('student_number'),
        )
        user.set_password(password)  # Hash the password
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update the user instance.
        """
        # Remove national_code if it is unchanged
        if 'national_code' in validated_data and instance.national_code == validated_data['national_code']:
            validated_data.pop('national_code')

        # Handle password update if provided
        password = validated_data.pop('password1', None)
        confirm_password = validated_data.pop('password2', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializers(serializers.Serializer):
    
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(
        label= ("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
    