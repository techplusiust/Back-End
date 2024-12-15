
from rest_framework import serializers
from .models import Comment
from accounts.models import CustomUser
from .models import Professor

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Displaying user fullname
    professor = serializers.StringRelatedField()  # Displaying professor name
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'professor_id', 'text']



## we do not add professors using an api, so do not need a serializer
# class ProfessorSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Professor
#         fields = ['id', 'name', 'department', 'comments']
