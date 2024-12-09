from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm, CreatePostForm, UserProfileSettingsForm, CommentForm
from .models import Post, UserProfile, Comment


def feed(request):
    if not request.user.is_anonymous:
        context = {
            'username': request.user.username
        }
        return render(request, 'feed/feed.html', context)

    return HttpResponseRedirect(reverse('feed:login'))


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('feed:feed'))

    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('feed:login'))

    form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('feed:login'))


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES['content']
            description = request.POST['description']
            Post.objects.create(user=request.user, content=content, description=description)

            return HttpResponseRedirect(reverse('feed:profile', kwargs={'username': request.user.username}))
    else:
        form = CreatePostForm()
    context = {'form': form, 'username': request.user.username}
    return render(request, 'posts/create_post.html', context)


def post(request, post_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('feed:login'))

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(author=request.user, post_id=post_id, text=request.POST.get('text'))
            return HttpResponseRedirect(reverse('feed:post', kwargs={'post_id': post_id}))

    post_ = Post.objects.get(id=post_id)
    context = {
        'post': post_,
        'is_user_liked': post_.likes.filter(username=request.user.username).exists(),
        'username': request.user.username,
        'form': CommentForm(),
    }
    return render(request, 'posts/post.html', context)


def profile(request, username=None):
    if username is None:
        user_profile = UserProfile.objects.get(user__username=request.user.username)
    else:
        user_profile = UserProfile.objects.get(user__username=username)
    context = {
        'user_profile': user_profile,
        'username': request.user.username
    }
    return render(request, 'user_profile/user_profile.html', context)


def profile_settings(request):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            user_profile = UserProfile.objects.get(user__username=request.user.username)
            if request.FILES.get('profile_image', False):
                user_profile.profile_image = request.FILES['profile_image']
            user_profile.save()
            form = UserProfileSettingsForm(
                data=request.POST,
                instance=UserProfile.objects.get(user__username=request.user.username)
            )
            form.save()
            return HttpResponseRedirect(reverse('feed:profile', kwargs={'username': request.user.username}))

        form = UserProfileSettingsForm(instance=UserProfile.objects.get(user__username=request.user.username))
        context = {
            'form': form,
            'username': request.user.username,
        }
        return render(request, 'user_profile/profile_settings.html', context)
    return HttpResponseRedirect(reverse('feed:login'))
