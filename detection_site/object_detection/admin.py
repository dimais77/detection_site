from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ImageFeed, DetectedObject

admin.site.register(DetectedObject)
admin.site.register(ImageFeed)

