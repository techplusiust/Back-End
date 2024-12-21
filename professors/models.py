from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model


class Professor(models.Model):
    
    name_fa = models.CharField(max_length=254, null=False, unique=True)
    name_en = models.CharField(max_length=254, null=False, unique=True)
    
    department_fa = models.CharField(max_length=254)
    department_en = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.name_fa} / {self.name_en} {self.department_fa} / {self.department_en}"



class Comment(models.Model):
    professor = models.ForeignKey(Professor, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)  # Reference to CustomUser
    text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.fullname} on {self.professor}"