from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from feed.models import Post, UserProfile, Comment


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username_or_email', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите e-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(user=user)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'description']
        widgets = {
            'content': forms.FileInput(attrs={
                'type': 'file',
                'accept': 'image/*',
                'class': 'file-input'
            }),
            'description': forms.Textarea(attrs={
                'type': 'text',
                'class': 'description_input',
            }),
        }


class UserProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'second_name', 'description', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'class': 'first-name-input',
                'placeholder': 'Имя',
                'required': False,
            }),
            'second_name': forms.TextInput(attrs={
                'type': 'text',
                'class': 'second-name-input',
                'placeholder': 'Фамилия',
                'required': False,
            }),
            'description': forms.Textarea(attrs={
                'type': 'text',
                'class': 'description-input',
                'placeholder': 'Описание',
                'required': False,
            }),
            'profile_image': forms.FileInput(attrs={
                'type': 'file',
                'accept': 'image/*',
                'class': 'file-input',
                'required': False,
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'type': 'text',
                'class': 'text-input',
                'placeholder': 'Оставьте комментарий',
                'required': True,
                'oninput': 'autoResize()',
                'cols': False,
                'rows': False,
            })
        }
