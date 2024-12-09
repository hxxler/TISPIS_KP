from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from .models import UserProfile, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'posts']

    def save(self, **kwargs):
        user = super().save(**kwargs)

        UserProfile.objects.create(user=user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ['username']

    pagination_class = LimitOffsetPagination
    paginate_by = 10


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'second_name', 'description', 'profile_image', 'followers_count',
                  'followings_count', 'posts_count']
        read_only_fields = ['user', 'followers_count', 'followings_count', 'posts_count']

    def data_with_info(self, request_user):
        data = self.data.copy()
        data.update({
            'posts': [PostsSerializer(instance=Post.objects.get(id=post.id)).data for post in
                      self.instance.user.posts.all()],
            'is_user_subscribed': self.instance.followers.filter(username=request_user.username).exists()
        })
        return data


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'id', 'content', 'description', 'likes_count']
        read_only_fields = ['user', 'id', 'likes_count']

    def data_with_user_info(self, request_user):
        data = self.data.copy()
        data.update({
            'user': {'username': self.instance.user.username,
                     'profile_image': self.instance.user.user_profile.get().profile_image.url},
            'is_user_liked': self.instance.likes.filter(username=request_user.username).exists()
        })
        return data


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text']
        read_only_fields = ['id', 'author', 'post']

    def data_with_author_info(self):
        data = self.data.copy()
        data.update({
            'author': {'username': self.instance.author.username,
                       'profile_image': self.instance.author.user_profile.get().profile_image.url}
        })
        return data
