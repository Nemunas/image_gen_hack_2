from flask import Flask, request, make_response, send_from_directory
from flask_cors import CORS
import traceback
import json

import pandas as pd

app = Flask(__name__)
CORS(app)


from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_response(message, status_code):
    response = make_response(message, status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from all origins
    response.headers['Access-Control-Allow-Headers'] = '*'  # Allow all headers
    response.headers['Access-Control-Allow-Methods'] = '*'  # Allow all HTTP methods

    return response

@app.route('/process_image', methods=['POST'])
def process_image():
    # Retrieve the ID from the request
    # story_id = request.form.get('story_id')
    
    # Validate ID
    # if not story_id:
    #     return jsonify({"error": "ID is required"}), 400
    story_id = 1

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If user does not select file, browser might submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file.save(input_path)
        # Here you can run your function on the saved image
        result = run_function_on_image(input_path)
        # return jsonify()
        urls = ["http://ec2-18-170-44-95.eu-west-2.compute.amazonaws.com:5001/get_image/" + str(x) for x in result]
        return generate_response({"result": result, "urls": urls }, 200)

from dotenv import load_dotenv
from helpers import compose_images_from_json, remove_background

import os
load_dotenv()

api_key = os.environ['api_key']
input_path = os.path.join(UPLOAD_FOLDER, f"input_image.jpg")
output_path = os.path.join(UPLOAD_FOLDER, f"output_image.png")

def run_function_on_image(input_path):
    success = remove_background(input_path, output_path, api_key)

    if success:
        print("Background removal successful!")
    else:
        print("Failed to remove background.")

    story_keys = [
        's1_p1_village',
        's1_p2_boat', 
        's1_p3_forest_hut',
        's1_p4_lake',     
        's1_p5_treasure_room',     
    ]

    outputs = []

    for key in story_keys:
        print(key)
        output_image_name = f'{key}_composition_output.png'
        output_image_path = os.path.join(UPLOAD_FOLDER, output_image_name)
                
        compose_images_from_json(
            input_image_path = output_path,  
            json_path = f'backgrounds/{key}_composition.json',
            output_image_path = output_image_path
        )
        outputs.append(output_image_name)

    return outputs

@app.route('/get_image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
