from django.contrib.auth.models import User
from django.db import models
from stdimage import StdImageField


def get_user_profile_photo_path(instance, filename):
    username = instance.user.username
    return f"profile_photos/{username}/{filename}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(blank=True)
    second_name = models.CharField(blank=True)
    description = models.TextField(blank=True)

    profile_image = models.ImageField(upload_to=get_user_profile_photo_path, default="/profile_photos/admin/logo.jpg")
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    followings = models.ManyToManyField(User, related_name='followings', blank=True)
    followers_count = models.PositiveIntegerField(default=0)
    followings_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


def get_posts_photos_path(instance, filename):
    username = instance.user.username
    return f"posts_photo/{username}/{filename}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    content = StdImageField(upload_to=get_posts_photos_path)
    description = models.TextField(blank=True)

    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    likes_count = models.PositiveIntegerField(default=0)

    viewed_by = models.ManyToManyField(UserProfile, related_name='viewed_posts', blank=True)

    def __str__(self):
        return self.description[:15] if self.description[:1] else f"Post of {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user_profile = UserProfile.objects.get(user__username=self.user.username)
        user_profile.posts_count = User.objects.get(username=self.user.username).posts.count()
        user_profile.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        user_profile = UserProfile.objects.get(user__username=self.user.username)
        user_profile.posts_count = User.objects.get(username=self.user.username).posts.count()
        user_profile.save()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"{self.author.username}: Comment to {self.post}"
