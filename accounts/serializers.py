# accounts/serializers.py

from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate


class UserSerializer(UserCreationForm):
    confirm_password = serializers.CharField(
        write_only=True)  # Adding confirm password

    class Meta:
        # model = CustomUser
        model = get_user_model()
        # REQUIRED FIELDS
        fields = ['fullname', 'national_code', 'email', 'department', 'student_number']
        
        extra_kwargs = {
            # 'password': {'write_only': True},  # Password should be write-only
            # 'confirm_password': {'write_only': True}  # Confirm password should also be write-only
        }

    def validate(self, data):
        """
        Ensure that password and confirm_password match. 
        DJANGO DOES THIS AUTOMATICALLY
        """
        pass

    def create(self, validated_data):
        """
        Create a user with the provided validated data and the hashed password.
        """
        # password = validated_data.pop('confirm_password')  # Remove confirm_password since it's not stored
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Set the password properly (hashed)
        user.save()
        return user


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
    