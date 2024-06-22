from django.urls import path
from .views import (
    home, register, user_login, user_logout, dashboard,
    process_image_feed, add_image_feed, delete_image,
    password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'object_detection'

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('register/', register, name='register'),  # Страница регистрации
    path('login/', user_login, name='login'),  # Страница входа
    path('logout/', user_logout, name='logout'),  # Выход из аккаунта
    path('dashboard/', dashboard, name='dashboard'),  # Личный кабинет
    path('process/<int:feed_id>/', process_image_feed, name='process_feed'),  # Обработка изображения
    path('add-image-feed/', add_image_feed, name='add_image_feed'),  # Добавление изображения
    path('image/delete/<int:image_id>/', delete_image, name='delete_image'),  # Удаление изображения
    path('password_reset/', password_reset, name='password_reset'),  # Сброс пароля
    path('password_reset_done/', password_reset_done, name='password_reset_done'),  # Завершение сброса пароля
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),  # Подтверждение сброса пароля
    path('reset/done/', password_reset_complete, name='password_reset_complete'),  # Завершение процесса сброса пароля
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
