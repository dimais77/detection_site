from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ImageFeed
from .utils import process_image
from .forms import ImageFeedForm


# Create your views here.
def home(request):
    return render(request, 'object_detection/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('object_detection:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'object_detection/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('object_detection:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'object_detection/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('object_detection:login')


@login_required
def dashboard(request):
    image_feeds = ImageFeed.objects.filter(user=request.user)
    return render(request, 'object_detection/dashboard.html', {'image_feeds': image_feeds})


@login_required
def process_image_feed(request, feed_id):
    image_feed = get_object_or_404(ImageFeed, id=feed_id, user=request.user)
    process_image(feed_id)  # Consider handling this asynchronously
    return redirect('object_detection:dashboard')


@login_required
def add_image_feed(request):
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user
            image_feed.save()
            return redirect('object_detection:dashboard')
    else:
        form = ImageFeedForm()
    return render(request, 'object_detection/add_image_feed.html', {'form': form})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageFeed, id=image_id, user=request.user)  # Ensuring only the owner can delete
    image.delete()
    return redirect('object_detection:dashboard')
