from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model


class Professor(models.Model):
    name = models.CharField(max_length=254, null=False, unique=True)
    department = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.name} {self.department}"



class Comment(models.Model):
    professor = models.ForeignKey(Professor, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)  # Reference to CustomUser
    text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.fullname} on {self.professor}"