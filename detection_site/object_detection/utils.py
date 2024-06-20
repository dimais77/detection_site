import cv2
import numpy as np
from .models import ImageFeed, DetectedObject, DescribedImage
from django.core.files.base import ContentFile
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Метки классов для модели object detection
VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]

# Обработка изображения в зависимости от выбранной модели
def process_image(image_feed_id, model_type=None):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path

        if model_type == 'model_1':
            # Настройка и запуск модели для object detection
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
                        confidence=round(float(confidence), 2)
                    )

            text, encoded_img = cv2.imencode('.jpg', img)
            if text:
                content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
                image_feed.processed_image.save(content.name, content, save=True)

        elif model_type == 'model_2':
            # Настройка и запуск модели для описания изображения
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

            raw_image = Image.open(image_path).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            result = processor.decode(out[0], skip_special_tokens=True)

            if result:
                DescribedImage.objects.create(
                    image_feed=image_feed,
                    describe=result
                )
                return result

        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False
