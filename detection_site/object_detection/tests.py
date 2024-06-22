import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ImageFeed, DetectedObject, DescribedImage


User = get_user_model()

class ImageFeedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def test_image_feed_creation(self):
        image_feed = ImageFeed.objects.create(user=self.user, image=self.image)
        self.assertEqual(image_feed.user, self.user)
        self.assertTrue(os.path.exists(image_feed.image.path))

    def test_image_feed_deletion(self):
        image_feed = ImageFeed.objects.create(user=self.user, image=self.image)
        image_path = image_feed.image.path
        image_feed.delete()
        self.assertFalse(os.path.exists(image_path))

class DetectedObjectTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.image_feed = ImageFeed.objects.create(user=self.user, image=self.image)

    def test_detected_object_creation(self):
        detected_object = DetectedObject.objects.create(
            image_feed=self.image_feed,
            object_type='cat',
            confidence=0.95,
            location='50,50,100,100'
        )
        self.assertEqual(detected_object.object_type, 'cat')
        self.assertEqual(detected_object.confidence, 0.95)

class DescribedImageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.image_feed = ImageFeed.objects.create(user=self.user, image=self.image)

    def test_described_image_creation(self):
        described_image = DescribedImage.objects.create(
            image_feed=self.image_feed,
            describe='A cat sitting on a chair'
        )
        self.assertEqual(described_image.describe, 'A cat sitting on a chair')
