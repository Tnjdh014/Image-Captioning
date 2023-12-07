import streamlit as st
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, ViTImageProcessor, ViTForImageClassification
import time 
import random
import uuid
import pyperclip

st.title('Welcome to the Image Captionator!')
st.write('Upload an image and get a cool caption!')
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
    #st.write("Predicted class:", model.config.id2label[predicted_class_idx])
    pred_class = model.config.id2label[predicted_class_idx]

    #load SalesForce AI
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # img_url = 'https://farm5.staticflickr.com/4022/4684418248_197a995011_z.jpg' 
    raw_image = image.convert('RGB')

    # conditional image captioning
    unique_id = str(uuid.uuid4())
    text = st.write(f'**Items successfully pulled from photo:** {pred_class} - Unique ID: {unique_id}')

    inputs = processor(raw_image, text, return_tensors="pt")

    out = model.generate(**inputs)
    st.write(processor.decode(out[0], skip_special_tokens=True))

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

img_url = 'https://farm5.staticflickr.com/4022/4684418248_197a995011_z.jpg'
image = Image.open(requests.get(img_url, stream=True).raw)
#image_caption(image)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded Image', use_column_width=True)
    
    except Exception as e:
        st.error(f"Error: Cannot read file. Please upload an image file (png, jpg, jpeg)")

    # Add a "Generate Caption" button
    if st.button('Generate Caption'):
        with st.spinner('Generating Caption...'):
            # Simulate a delay to show the loading bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            
            generated_caption = image_caption(image)
            if "arafed" in generated_caption:
                generated_caption = generated_caption.replace("arafed", "A")
            st.success('Caption Generated!')
            output_placeholder = st.empty()
            output_placeholder.markdown(
            f'**Generated Caption:**<br>'
            f'<div style="border: 1px solid #a1a1a1; border-radius: 10px; cursor: pointer; text-align: center; padding: 10px" onclick="copyToClipboard(\'{generated_caption}\')">{generated_caption}</div>',
            unsafe_allow_html=True
            )
            
        
            # Call the image_caption function and display the result
            # generated_caption = image_caption(image)
           
            # st.success('Caption Generated!')
            # # st.write(f'**Generated Caption:** {generated_caption}')
            # st.markdown(
            # f'**Generated Caption:**<br>'
            # f'<div style="border: 1px solid #a1a1a1; border-radius: 10px; cursor: pointer; text-align: center; padding: 10px">{generated_caption}</div>',
            # unsafe_allow_html=True
            # )


