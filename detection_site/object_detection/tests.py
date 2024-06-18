import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": 'Bearer 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'}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("image_3.webp")
print(output)

# import os
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
#
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
#
# image_path = os.path.join(os.getcwd(), "image_1.jpg")
#
# raw_image = Image.open(image_path).convert('RGB')
#
# text = "A photography of"
# inputs = processor(raw_image, text, return_tensors="pt")
#
# out = model.generate(**inputs, max_new_tokens=50)
# print(processor.decode(out[0], skip_special_tokens=True))
#
# inputs = processor(raw_image, return_tensors="pt")
#
# out = model.generate(**inputs, max_new_tokens=50)
# print(processor.decode(out[0], skip_special_tokens=True))
