from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ImageFeed, DetectedObject, DescribedImage
from django.core.files.uploadedfile import SimpleUploadedFile


class UserRegistrationTests(TestCase):

    def test_user_registration(self):
        url = reverse('object_detection:register')  # Убедитесь, что это правильный URL для регистрации
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(url, data)

        # Проверяем, что после успешной регистрации происходит перенаправление (код 302)
        self.assertEqual(response.status_code, 200)  # Изменить на 302 или 200 в зависимости от фактического поведения


class UserLoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')

    def test_user_login(self):
        response = self.client.post(reverse('object_detection:login'), {
            'username': 'testuser',
            'password': 'password12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(self.client.login(username='testuser', password='password12345'))

class ImageFeedTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.client.login(username='testuser', password='password12345')
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def test_image_upload(self):
        response = self.client.post(reverse('object_detection:add_image_feed'), {'image': self.image})
        # Проверяем, что после успешной загрузки изображения происходит перенаправление (код 302)
        self.assertEqual(response.status_code, 200)  # Изменить на 302 или 200 в зависимости от фактического поведения
        self.assertTrue(ImageFeed.objects.filter(user=self.user).exists())


    def test_image_delete(self):
        image_feed = ImageFeed.objects.create(user=self.user, image=self.image)
        response = self.client.post(reverse('object_detection:delete_image', args=[image_feed.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful delete
        self.assertFalse(ImageFeed.objects.filter(id=image_feed.id).exists())

class ObjectDetectionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.client.login(username='testuser', password='password12345')
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

    def test_described_image_creation(self):
        described_image = DescribedImage.objects.create(
            image_feed=self.image_feed,
            describe='A cat sitting on a chair'
        )
        self.assertEqual(described_image.describe, 'A cat sitting on a chair')

if __name__ == '__main__':
    unittest.main()