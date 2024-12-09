from django.urls import path
from rest_framework.routers import DefaultRouter

from api.serializers import UserViewSet
from api.views import ObtainAuthTokenView, RegisterUserView, ProfileView, PostView, like_post, remove_like, \
    get_new_posts, CommentsView, get_comments, subscribe, unsubscribe, documentation

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('login', ObtainAuthTokenView.as_view(), name='login'),
    path('register', RegisterUserView.as_view(), name='register'),

    path('profile', ProfileView.as_view(), name='update_profile'),
    path('subscribe', subscribe, name='subscribe'),
    path('unsubscribe', unsubscribe, name='unsubscribe'),

    path('post', PostView.as_view(), name='post'),
    path('get-new-posts', get_new_posts, name='get_new_posts'),
    path('like-post', like_post, name='like_post'),
    path('remove-like', remove_like, name='remove_like'),

    path('comment', CommentsView.as_view(), name='post'),
    path('get-comments', get_comments, name='get_comments'),

    path('docs', documentation, name='documentation'),
] + router.urls

