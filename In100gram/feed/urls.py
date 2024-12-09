from django.urls import path

from feed import views

app_name = 'feed'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:post_id>', views.post, name='post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
]
