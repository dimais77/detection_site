from django.urls import path

from .views import home, register, user_login, user_logout, dashboard, process_image_feed, add_image_feed, delete_image

from django.conf import settings
from django.conf.urls.static import static

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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
