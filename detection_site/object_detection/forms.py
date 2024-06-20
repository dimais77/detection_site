from django import forms
from .models import ImageFeed
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Форма для загрузки изображения
class ImageFeedForm(forms.ModelForm):
    image = forms.ImageField(label='', widget=forms.FileInput(attrs={'accept': 'image/*'}))  # Поле для загрузки изображения

    class Meta:
        model = ImageFeed
        fields = ['image']

# Кастомизированная форма регистрации пользователя
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()  # Добавление поля email к стандартной форме

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
