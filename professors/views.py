# comments/views.py

from .serializers import CommentSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Comment, Professor
from accounts.models import CustomUser
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_professors(request):
    professors = Professor.objects.all()  # Query all users from CustomUser
    professors_data = [
        {"id": professor.id,
         "name": {
             "en": professor.name_en,
             "fa": professor.name_fa
         },
         "department": {
             "en": professor.department_en,
             "fa": professor.department_fa
         }
         }
        for professor in professors]

    return Response(professors_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_professor_with_comments(request, id):
    professor = get_object_or_404(Professor, id=id)
    comments = professor.comments.all()
    serialized_comments = CommentSerializer(comments, many=True)
    return Response({
        "id": professor.id,
         "name": {
             "en": professor.name_en,
             "fa": professor.name_fa
         },
         "department": {
             "en": professor.department_en,
             "fa": professor.department_fa
         },
        'comments': serialized_comments.data
    })


@api_view(['POST'])
# Only authenticated users can access this view
@permission_classes([IsAuthenticated])
def add_comment(request):
    try:
        # Get professor ID from form
        professor_id = request.data['professor_id']

        text = request.data['text']  # Get comment text from form

        professor = get_object_or_404(
            Professor, id=professor_id)  # Fetch the professor

        # Create and save the comment
        comment = Comment.objects.create(
            professor=professor,
            user=request.user,  # Use the logged-in user
            text=text
        )

        # Return a response, e.g., success message
        return JsonResponse({'message': 'Comment added successfully', 'comment_id': comment.id}, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Invalid request {e}'}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from professors.models import Professor

class FacultyListView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

    def get(self, request, *args, **kwargs):
        """Return a list of distinct faculties in both English and Persian."""
        faculties = Professor.objects.values('department_en', 'department_fa').distinct()
        return Response({"faculties": list(faculties)})

"""
# Add a comment for a professor
@api_view(['POST'])
@login_required
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        professor_id = request.data['id']  # Get professor ID from form

        text = request.POST.get('text')  # Get comment text from form

        professor = get_object_or_404(Professor, id=professor_id)  # Fetch the professor

        # Create and save the comment
        comment = Comment.objects.create(
            professor=professor,
            user=request.user,  # Use the logged-in user
            text=text
        )

        # Return a response, e.g., success message
        return JsonResponse({'message': 'Comment added successfully', 'comment_id': comment.id}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
"""


# View all comments for a specific professor
def view_comments(request, professor_id):
    professor = get_object_or_404(
        Professor, id=professor_id)  # Get the professor
    comments = professor.comments.all()  # Get all comments for this professor

    # Serialize comments to return in a response
    comments_data = [
        {
            'user': comment.user.fullname,  # User who made the comment
            'text': comment.text,  # Comment text
            # Optional, if you have `created_at` in your model
            'created_at': comment.created_at,
        }
        for comment in comments
    ]

    # Return the list of comments
    return JsonResponse({'professor': professor.name, 'comments': comments_data}, status=200)
