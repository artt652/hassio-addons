from flask import Flask, request, send_file, render_template
from PIL import Image
import cv2
import numpy as np
import io

app = Flask(__name__)

# Serve the homepage (frontend)
@app.route('/')
def home():
    return render_template('index.html')

def convert_image_to_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv_gray = 255 - gray_image
    blurred = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    inverted_blur = 255 - blurred
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    return sketch

# Handle image upload and conversion
@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    img = Image.open(file.stream)
    
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    sketch = convert_image_to_sketch(img_cv)
    
    is_success, buffer = cv2.imencode(".png", sketch)
    io_buf = io.BytesIO(buffer)
    
    return send_file(io_buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)