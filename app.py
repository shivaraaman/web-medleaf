import os
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import uuid
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\Users\shiva\Downloads\web\imgs"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the new model
def load_new_model(model_path):
    try:
        new_model = load_model(model_path)
        return new_model
    except Exception as e:
        print("Error loading new model:", e)
        return None

# Define the new classify function
def classify(image_path, model):
    try:
        print("Image path:", image_path)  # Print image path for debugging
        if not os.path.isfile(image_path):
            raise FileNotFoundError("Image file not found")
        
        image = Image.open(image_path)
        preprocessed_image = preprocess_image(image)
        predictions = model.predict(preprocessed_image)
        predicted_class_index = np.argmax(predictions)
        predicted_class = int(predicted_class_index)
        infoofindex = infoextract(predicted_class)
        print(infoofindex)
        return {'info': infoofindex}
    except Exception as e:
        return {'error': str(e)}

# Define the preprocess_image function (if not defined already)
def preprocess_image(image):
    image = image.resize((128, 128))
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Define the infoextract function (if not defined already)
def infoextract(indexnum):
    df = pd.read_csv(r'C:\Users\shiva\Downloads\web\data\plant_classification.csv')
    a = df['Botanical Name'][indexnum]
    l = [df['Botanical Name'][indexnum], df['Common Name'][indexnum], df['Family'][indexnum], df['Bioactive Compounds'][indexnum], df['Traditional Uses'][indexnum]]
    return l

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        image_data = request.files['image']
        if image_data.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = str(uuid.uuid4()) + '.png'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_data.save(image_path)

        # Load the new model
        model_path = r"C:\Users\shiva\Downloads\web\model\final_data.h5"
        new_model = load_new_model(model_path)
        if new_model is None:
            return jsonify({'error': 'Failed to load new model'}), 500

        # Classify the image using the new model
        result = classify(image_path, new_model)
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
