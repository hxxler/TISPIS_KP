# Generated by Django 4.2.2 on 2023-06-16 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feed.models
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('profile_image', models.ImageField(blank=True, upload_to='profile_images/')),
                ('followers', models.ManyToManyField(blank=True, to='feed.follower')),
                ('followings', models.ManyToManyField(blank=True, to='feed.following')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', stdimage.models.StdImageField(force_min_size=False, upload_to=feed.models.get_posts_photos_path, variations={})),
                ('description', models.TextField(blank=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feed.post')),
            ],
        ),
    ]