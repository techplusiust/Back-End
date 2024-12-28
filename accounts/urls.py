from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('users/', views.get_all_users, name='get_all_users'), 
    path('test_token/', views.test_token, name='test_token'), 
    path('users/<int:user_id>/edit/', views.edit_user, name='edit-user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete-user'),
    path('users/<int:user_id>/make-superuser/', views.make_superuser, name='make-superuser'),

]
