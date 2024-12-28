from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.shortcuts import render, get_object_or_404

from .models import CustomUser  # Import the custom user model
# Create your views here.

from django.contrib.auth import authenticate
from django.http import JsonResponse
from .serializers import UserSerializer, LoginSerializers
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def signup(request):

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
    # TOOD: Later, check whether  more data are needed to be returned from the user

    user = get_object_or_404(CustomUser, email=request.data["email"])

    if not user.check_password(request.data["password"]):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)

    serializer = LoginSerializers(instance=user)
    return Response(
        {
            "token": token.key,
            "user": serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request, user_id):
    """
    Allow users to edit their own information.
    """
    if not request.user.is_superuser:  # Ensure only superusers can edit
        return Response({"detail": "You are not allowed to edit users."}, status=status.HTTP_403_FORBIDDEN)
    
    if not request.user.is_superuser and request.user.id != user_id:
        return Response({"detail": "You are not allowed to edit this user."}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Pass the instance and request data correctly to the serializer
    serializer = UserSerializer(
        instance=user, data=request.data)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """
    Allow deletion of a user only if the requester has the required permissions.
    """
    if request.user.id == user_id:
        return Response({"detail": "You are not allowed to delete yourself."}, status=status.HTTP_403_FORBIDDEN)

    print(request.user.is_superuser, request.user.id, user_id)
    if not request.user.is_superuser:  # Ensure only superusers can delete
        return Response({"detail": "You are not allowed to delete users."}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_users(request):
    """
    View to return all users from the database.
    """
    users = CustomUser.objects.all()  # Query all users from CustomUser
    user_data = [{"id": user.id,
                  "fullname": user.fullname,
                  "national_code": user.national_code,
                  "email": user.email,
                  "department": user.department,
                  "student_number": user.student_number,
                  "is_superuser": user.is_superuser,
                  }
                 for user in users]

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"passed for {}".format(request.user.email)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_superuser(request, user_id):
    """
    API to make a user a superuser.
    Only existing superusers can perform this action.
    """
    # Check if the requesting user is a superuser
    if not request.user.is_superuser:
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        # Get the user to be updated
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response(
            {"detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Make the user a superuser
    user.is_superuser = True
    user.save()

    return Response(
        {"detail": f"User {user.fullname} ({user.email}) is now a superuser."},
        status=status.HTTP_200_OK,
    )
