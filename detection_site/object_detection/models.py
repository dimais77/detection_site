from django.db import models
from django.conf import settings
import os

# Модель ImageFeed представляет загруженные пользователем изображения
class ImageFeed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Пользователь, загрузивший изображение
    image = models.ImageField(upload_to='images/')  # Оригинальное изображение
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)  # Обработанное изображение

    def __str__(self):
        return f"{self.user.username} - {self.image.name}"

    def delete(self, *args, **kwargs):
        # Удаление связанных файлов при удалении объекта
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        if self.processed_image and os.path.isfile(self.processed_image.path):
            os.remove(self.processed_image.path)
        super().delete(*args, **kwargs)

# Модель DetectedObject представляет распознанные объекты в изображении
class DetectedObject(models.Model):
    image_feed = models.ForeignKey(ImageFeed, related_name='detected_objects', on_delete=models.CASCADE)  # Связь с ImageFeed
    object_type = models.CharField(max_length=100)  # Тип объекта (например, 'person', 'dog')
    confidence = models.FloatField()  # Уверенность модели в правильности распознавания
    location = models.CharField(max_length=255)  # Координаты объекта на изображении

    def __str__(self):
        return f"{self.object_type} ({self.confidence * 100}%) on {self.image_feed.image.name}"

# Модель DescribedImage представляет описание изображения
class DescribedImage(models.Model):
    image_feed = models.ForeignKey(ImageFeed, related_name='described_image', on_delete=models.CASCADE)  # Связь с ImageFeed
    describe = models.CharField(max_length=100)  # Описание изображения

    def __str__(self):
        return f"{self.describe}"
