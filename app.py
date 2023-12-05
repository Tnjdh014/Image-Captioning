from flask import Flask, jsonify, request
from PIL import Image
import requests
from ImageCaptioning import image_caption

app = Flask(__name__)


@app.route('/caption-image', methods=['POST', 'GET'])
def caption_image():
    try:
        # Ensure the request contains JSON data
        data = request.json
        if 'image_url' in data:
            image_url = data['image_url']
            # Download the image using the provided URL
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image = Image.open(response.raw)
                img_caption = image_caption(image)
                # Process the image using the image captioning code
                # Replace this with  actual image captioning logic
                # ...
                # Placeholder for generated caption
                generated_caption = img_caption
                # Return the generated caption
                return jsonify({'caption': generated_caption})
            else:
                return jsonify({'error': 'Failed to download image'})
        else:
            return jsonify({'error': 'Image URL not provided'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
