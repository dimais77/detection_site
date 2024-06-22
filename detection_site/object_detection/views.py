from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import ImageFeed, DetectedObject, DescribedImage
from .utils import process_image
from .forms import ImageFeedForm, CustomUserCreationForm

# Главная страница
def home(request):
    return render(request, 'object_detection/home.html')

# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('object_detection:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'object_detection/register.html', {'form': form})

# Вход пользователя
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

# Выход пользователя (доступно только авторизованным пользователям)
@login_required
def user_logout(request):
    logout(request)
    return redirect('object_detection:login')

# Личный кабинет (доступно только авторизованным пользователям)
@login_required
def dashboard(request):
    image_feeds = ImageFeed.objects.filter(user=request.user)
    detected_objects = DetectedObject.objects.filter(image_feed__in=image_feeds)
    describe_images = DescribedImage.objects.filter(image_feed__in=image_feeds)
    return render(request, 'object_detection/dashboard.html', {
        'image_feeds': image_feeds,
        'detected_objects': detected_objects,
        'describe_images': describe_images
    })

# Обработка изображения (доступно только авторизованным пользователям)
@login_required
def process_image_feed(request, feed_id):
    image_feed = get_object_or_404(ImageFeed, id=feed_id)
    model_type = request.POST.get('model_type', 'model_1')
    success = process_image(image_feed.id, model_type)
    if success:
        return redirect('object_detection:dashboard')
    else:
        return redirect('object_detection:dashboard')

# Добавление нового изображения (доступно только авторизованным пользователям)
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

# Удаление изображения (доступно только авторизованным пользователям)
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageFeed, id=image_id, user=request.user)
    image.delete()
    return redirect('object_detection:dashboard')

# Сброс пароля (начало процесса)
def password_reset(request):
    if request.method == 'POST':
        form = auth_views.PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='object_detection/password_reset_email.html',
                subject_template_name='object_detection/password_reset_subject.txt'
            )
            return redirect('object_detection:password_reset_done')
    else:
        form = auth_views.PasswordResetForm()
    return render(request, 'object_detection/password_reset.html', {'form': form})

# Завершение сброса пароля
def password_reset_done(request):
    return render(request, 'object_detection/password_reset_done.html')

# Подтверждение сброса пароля
def password_reset_confirm(request, uidb64=None, token=None):
    return render(request, 'object_detection/password_reset_confirm.html')
    # return auth_views.PasswordResetConfirmView.as_view(template_name='object_detection/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

# Завершение процесса сброса пароля
def password_reset_complete(request):
    return render(request, 'object_detection/password_reset_complete.html')
