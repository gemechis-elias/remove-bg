
# A very simple Flask Hello World app for you to get started with...

# from flask import Flask

# app = Flask(__name__)


from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64
import os
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Your Server is live and APIs is working! 🚀'

# Configure CORS
CORS(
    app,
    resources={r"/remove-bg": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["API-Key", "Content-Type"],
)

@app.route('/remove-bg', methods=["GET"])
def remove_bg_defualt():
    return 'Your Server is live and APIs is working! 🚀'

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    # Check if the image is part of the request
    if "image" not in request.files:
        return jsonify({"status": "error", "message": "No image file found in request"}), 400

    image_file = request.files["image"]

    # Validate the image file
    if image_file.filename == "":
        return jsonify({"status": "error", "message": "Empty filename provided"}), 400

    try:
        # Read image file into bytes
        input_image = image_file.read()

        # Remove background
        output_image_data = remove(input_image)

        # Encode the output image to base64
        encoded_image = base64.b64encode(output_image_data).decode('utf-8')

        return jsonify({
            "status": "success",
            "message": "Successfully generated",
            "image": encoded_image
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Expose the WSGI application callable as 'application'
application = app

if __name__ == "__main__":
    # It's recommended to run Flask with a production-ready server like Gunicorn
    app.run(host="0.0.0.0", port=5000, debug=False)