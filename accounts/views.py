from django.shortcuts import render

from .models import CustomUser  # Import the custom user model
# Create your views here.

from django.contrib.auth import authenticate
from django.http import JsonResponse
from .serializers import UserSerializer, LoginSerializers

from rest_framework.response import Response  # Add this import
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def signup(request):
    """
    View to handle user signup.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(email=request.data["email"])
        user.set_password(request.data["password1"])
        user.save()
        token = Token.objects.create(user=user)

        return Response(
            {
                "token": token.key,
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    View to handle user login.
    If the user exists and the password matches, return a welcome message.
    """
    # serializer = LoginSerializer(data=request.data)
    serializer = LoginSerializers(
        data=request.data, context={'request': request})

    if serializer.is_valid():

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            return JsonResponse({"message": f"Welcome back, {user.fullname}!"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_users(request):
    """
    View to return all users from the database.
    """
    users = CustomUser.objects.all()  # Query all users from CustomUser
    user_data = [{"fullname": user.fullname,
                  "national_code": user.national_code,
                  "email": user.email,
                  "department": user.department,
                  "student_number": user.student_number}
                 for user in users]

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def test_token(request):
    return Response({})
