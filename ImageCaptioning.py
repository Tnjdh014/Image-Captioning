import streamlit as st
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, ViTImageProcessor, ViTForImageClassification

st.title('hello')
uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "png", "jpg", "pdf"])

#Load Google IMage 
def image_caption(image):

    # img_url = 'https://farm5.staticflickr.com/4022/4684418248_197a995011_z.jpg'
    # image = Image.open(requests.get(img_url, stream=True).raw)

    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    # model predicts one of the 1000 ImageNet classes
    predicted_class_idx = logits.argmax(-1).item()
    st.write("Predicted class:", model.config.id2label[predicted_class_idx])
    pred_class = model.config.id2label[predicted_class_idx]



    #load SalesForce AI
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # img_url = 'https://farm5.staticflickr.com/4022/4684418248_197a995011_z.jpg' 
    raw_image = image.convert('RGB')

    # conditional image captioning

    text = f'a photo of {pred_class}'
    inputs = processor(raw_image, text, return_tensors="pt")

    out = model.generate(**inputs)
    st.write(processor.decode(out[0], skip_special_tokens=True))

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

img_url = 'https://farm5.staticflickr.com/4022/4684418248_197a995011_z.jpg'
image = Image.open(requests.get(img_url, stream=True).raw)
# image_caption(image)
