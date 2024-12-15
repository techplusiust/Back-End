# comments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_professors, name='get_professors'),  # get  all professor
]