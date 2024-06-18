import cv2
import numpy as np
import requests
from .models import ImageFeed, DetectedObject
from django.conf import settings
from django.core.files.base import ContentFile

VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]

def process_image(image_feed_id, model_type='local'):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path

        if model_type == 'local':
            model_path = 'object_detection/mobilenet_iter_73000.caffemodel'
            config_path = 'object_detection/mobilenet_ssd_deploy.prototxt'
            net = cv2.dnn.readNetFromCaffe(config_path, model_path)

            img = cv2.imread(image_path)
            if img is None:
                print("Failed to load image")
                return False

            h, w = img.shape[:2]
            blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.6:
                    class_id = int(detections[0, 0, i, 1])
                    class_label = VOC_LABELS[class_id]
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    label = f"{class_label}: {confidence:.2f}"
                    cv2.putText(img, label, (startX + 5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    DetectedObject.objects.create(
                        image_feed=image_feed,
                        object_type=class_label,
                        location=f"{startX},{startY},{endX},{endY}",
                        confidence=float(confidence)
                    )

            result, encoded_img = cv2.imencode('.jpg', img)
            if result:
                content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
                image_feed.processed_image.save(content.name, content, save=True)

        elif model_type == 'api':
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
            headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}

            with open(image_path, "rb") as f:
                data = f.read()

            response = requests.post(API_URL, headers=headers, data=data)
            results = response.json()

            # Проверяем, что результат является списком с одним словарем
            if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
                obj = results[0]  # Получаем первый словарь из списка

                # Получаем текстовый результат из ключа 'generated_text'
                generated_text = obj.get('generated_text', 'No generated text found')

                # Создаем объект DetectedObject с полученными данными
                DetectedObject.objects.create(
                    image_feed=image_feed,
                    object_type=generated_text,
                    location="0,0,0,0",  # Укажите корректное значение, если доступно из API
                    confidence=1.0  # Укажите корректное значение уверенности, если доступно из API
                )

        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False



# import cv2
# import numpy as np
# from django.core.files.base import ContentFile
# from .models import ImageFeed, DetectedObject
#
# VOC_LABELS = [
#     "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
#     "bus", "car", "cat", "chair", "cow", "diningtable",
#     "dog", "horse", "motorbike", "person", "pottedplant",
#     "sheep", "sofa", "train", "tvmonitor"
# ]
#
#
# def process_image(image_feed_id):
#     try:
#         image_feed = ImageFeed.objects.get(id=image_feed_id)
#         image_path = image_feed.image.path
#
#         model_path = 'object_detection/mobilenet_iter_73000.caffemodel'
#         config_path = 'object_detection/mobilenet_ssd_deploy.prototxt'
#         net = cv2.dnn.readNetFromCaffe(config_path, model_path)
#
#         img = cv2.imread(image_path)
#         if img is None:
#             print("Failed to load image")
#             return False
#
#         h, w = img.shape[:2]
#         blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)
#
#         net.setInput(blob)
#         detections = net.forward()
#
#         for i in range(detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.6:
#                 class_id = int(detections[0, 0, i, 1])
#                 class_label = VOC_LABELS[class_id]
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
#                 label = f"{class_label}: {confidence:.2f}"
#                 cv2.putText(img, label, (startX + 5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#                 DetectedObject.objects.create(
#                     image_feed=image_feed,
#                     object_type=class_label,
#                     location=f"{startX},{startY},{endX},{endY}",
#                     confidence=float(confidence)
#                 )
#
#         result, encoded_img = cv2.imencode('.jpg', img)
#         if result:
#             content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
#             image_feed.processed_image.save(content.name, content, save=True)
#
#         return True
#
#     except ImageFeed.DoesNotExist:
#         print("ImageFeed not found.")
#         return False
