from django.urls import path

from .views import home, register, user_login, user_logout, dashboard, process_image_feed, add_image_feed, delete_image, \
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'object_detection'

urlpatterns = [
                  path('', home, name='home'),
                  path('register/', register, name='register'),
                  path('login/', user_login, name='login'),
                  path('logout/', user_logout, name='logout'),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('process/<int:feed_id>/', process_image_feed, name='process_feed'),
                  path('add-image-feed/', add_image_feed, name='add_image_feed'),
                  path('image/delete/<int:image_id>/', delete_image, name='delete_image'),
                  path('password_reset/', password_reset, name='password_reset'),
                  path('password_reset_done/', password_reset_done, name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
                  path('reset/done/', password_reset_complete, name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
