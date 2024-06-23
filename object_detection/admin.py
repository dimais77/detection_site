from django.contrib import admin
from .models import ImageFeed, DetectedObject, DescribedImage

# Регистрация моделей в административной панели Django
admin.site.register(ImageFeed)
admin.site.register(DetectedObject)
admin.site.register(DescribedImage)
