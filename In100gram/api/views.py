from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.db.models import Q

from api.serializers import UserSerializer, UserProfileSerializer, PostsSerializer, CommentsSerializer
from .models import UserProfile, Post, Comment


class ObtainAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'token': 'Invalid credentials'}, status=403)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']

            try:
                validate_password(password)
            except ValidationError as e:
                return Response({'error': e.messages}, status=400)

            hashed_password = make_password(password)
            serializer.save(password=hashed_password)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        username = request.data.get('username', request.user.username)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'username': "UserProfile not found."}, status=404)
        profile_serializer = UserProfileSerializer(instance=UserProfile.objects.get(user__username=user.username))
        return Response(profile_serializer.data_with_info(request.user))

    @staticmethod
    def put(request):
        serializer = UserProfileSerializer(data=request.data,
                                           instance=UserProfile.objects.get(user__username=request.user.username))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data_with_info(request.user))
        return Response(serializer.errors, status=400)

    @staticmethod
    def delete(request):
        User.objects.get(username=request.user.username).delete()
        return Response({'message': "User deleted successfully."}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribe(request):
    try:
        following = UserProfile.objects.get(user__id=request.data.get('user_id'))
    except UserProfile.DoesNotExist:
        return Response({'user_id': "User not found."}, status=404)

    if following.followers.filter(username=request.user.username).exists():
        return Response({'error': "You already subscribed to this user."}, status=405)

    if request.user.username == following.user.username:
        return Response({'error': "You cannot subscribe to yourself."}, status=405)

    following.followers.add(request.user)
    user_profile = request.user.user_profile.get()
    user_profile.followings.add(following.user)
    return Response(UserProfileSerializer(instance=following).data_with_info(request.user))


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def unsubscribe(request):
    try:
        following = UserProfile.objects.get(user__id=request.data.get('user_id'))
    except UserProfile.DoesNotExist:
        return Response({'user_id': "User not found."}, status=404)

    if not following.followers.filter(username=request.user.username).aexists():
        return Response({'error': "You haven't already subscribed to this user."}, status=405)

    if request.user.username == following.user.username:
        return Response({'error': "You cannot unsubscribe to yourself."}, status=405)

    following.followers.remove(request.user)
    user_profile = request.user.user_profile.get()
    user_profile.followings.remove(following.user)
    return Response(UserProfileSerializer(instance=following).data_with_info(request.user))


class PostView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            post = Post.objects.get(id=request.query_params.get('id'))
        except Post.DoesNotExist:
            return Response({'id': "Post not found."}, status=404)
        serializer = PostsSerializer(instance=post)
        return Response(serializer.data_with_user_info(request.user))

    @staticmethod
    def post(request):
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data_with_user_info(request.user))
        return Response(serializer.errors, status=400)

    @staticmethod
    def put(request):
        try:
            post = Post.objects.get(id=request.data.get('id'))
        except Post.DoesNotExist:
            return Response({'id': "Post not found."}, status=400)

        if post.user.username != request.user.username:
            return Response({'detail': "You haven't access."}, status=403)

        data = request.data.copy()
        if not data.get('content'):
            data.update({'content': post.content})
        post = PostsSerializer(data=data, instance=post)

        if post.is_valid():
            post.save()
            return Response(post.data_with_user_info(request.user))
        return Response(post.errors, status=400)

    @staticmethod
    def delete(request):
        try:
            post = Post.objects.get(id=request.data.get('id'))
        except Post.DoesNotExist:
            return Response({'id': "Post not found."}, status=400)

        if post.user.username != request.user.username:
            return Response({'detail': "You haven't access."}, status=403)

        post.delete()
        return Response({'message': "Post deleted successfully."}, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_new_posts(request):
    user_profile = UserProfile.objects.get(user__username=request.user.username)
    followings = user_profile.followings.all()
    posts = Post.objects.filter(~Q(id__in=user_profile.viewed_posts.all()), user__in=followings)[:10]
    new_posts = []
    if len(posts) < 10:
        posts = posts.union(
            Post.objects.filter(~Q(id__in=user_profile.viewed_posts.all()), ~Q(user__in=followings))[:10 - len(posts)])
    for post in posts:
        serializer = PostsSerializer(instance=post)
        new_posts.append(serializer.data_with_user_info(request.user))
        # post.viewed_by.add(user_profile)
    return Response(new_posts)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request):
    try:
        post = Post.objects.get(id=request.data.get('id'))
    except Post.DoesNotExist:
        return Response({'error': "Post not found."}, status=400)

    try:
        post.likes.get(username=request.user.username)
    except User.DoesNotExist:
        post.likes.add(request.user)
        post.likes_count += 1
        post.save()
    else:
        return Response({'error': "You already liked this post."}, status=405)
    serializer = PostsSerializer(instance=post)
    return Response(serializer.data_with_user_info(request.user), status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_like(request):
    try:
        post = Post.objects.get(id=request.data.get('id', None))
    except Post.DoesNotExist:
        return Response({'id': "Post not found."}, status=400)

    try:
        post.likes.get(username=request.user.username)
    except User.DoesNotExist:
        return Response({'error': "You haven't liked this post yet."}, status=405)
    else:
        post.likes.remove(request.user)
        post.likes_count -= 1
        post.save()
    serializer = PostsSerializer(instance=post)
    return Response(serializer.data_with_user_info(request.user), status=200)


class CommentsView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            serializer = CommentsSerializer(instance=Comment.objects.get(id=request.data.get('id')))
        except Comment.DoesNotExist:
            return Response({'id': "Comment not found."}, status=404)
        return Response(serializer.data_with_author_info())

    @staticmethod
    def post(request):
        author = request.user
        try:
            post = Post.objects.get(id=request.data.get('post'))
        except Post.DoesNotExist:
            return Response({'post': 'Post not found.'}, status=404)
        text = request.data.get('text')
        if text is None:
            return Response({'text': "Text is empty."}, status=400)
        serializer = CommentsSerializer(data=request.data, instance=Comment(author=author, post=post, text=text))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @staticmethod
    def put(request):
        try:
            comment = Comment.objects.get(id=request.data.get('id'))
        except Comment.DoesNotExist:
            return Response({'id': "Comment not found."}, status=404)
        if comment.author.username != request.user.username:
            return Response({'detail': "Yoy haven't access."}, status=403)
        serializer = CommentsSerializer(data=request.data, instance=comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @staticmethod
    def delete(request):
        try:
            comment = Comment.objects.get(id=request.data.get('id'))
        except Comment.DoesNotExist:
            return Response({'id': "Comment not found."}, status=404)
        if comment.author.username != request.user.username:
            return Response({'detail': "Yoy haven't access."}, status=403)
        comment.delete()
        return Response({'message': "Comment deleted successfully."}, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_comments(request):
    post_id, part_number = request.query_params.get('post_id'), request.query_params.get('part_number')
    if post_id is None:
        return Response({'post_id': "You didn't enter id."}, status=400)
    if part_number is None or (isinstance(part_number, str) and not part_number.isdigit()):
        return Response({'part_number': "You didn't enter part_number."}, status=400)
    part_number = int(part_number)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'post_id': "Post not found."}, status=404)

    comments = post.comments.all()[(part_number - 1) * 10: part_number * 10]
    return Response([CommentsSerializer(instance=comment).data_with_author_info() for comment in comments])


def documentation(request):
    return render(request, 'documentation/index.html')
