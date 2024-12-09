from django.contrib import admin

from feed.models import Post, UserProfile, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
