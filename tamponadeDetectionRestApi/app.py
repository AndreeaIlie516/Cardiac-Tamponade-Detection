from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import prediction
import os

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


class Test(Resource):
    def get(self):
        return 'Welcome to, Test App API!'
    def post(self):
        try:
            value = request.get_json()
            if value:
                return {'Post Values': value}, 201

            return {"error": "Invalid format."}

        except Exception as error:
            return {'error': error}


class GetPredictionOutput(Resource):
    def get(self):
        return {"error": "Invalid Method."}

    def post(self):
        try:
            # Check if an image file was uploaded
            if 'image' not in request.files:
                return {"error": "No image file provided"}, 400

            image_file = request.files['image']
            if image_file:
                # # Convert the image to an OpenCV format
                # image = Image.open(BytesIO(image_file.read()))
                # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)

                # Decode the image from bytes
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                print("Image:", image)

                if image is None:
                    return {"error": "Invalid image format or corrupted file"}, 400
                # Process and predict using your existing logic
                tamponadeDetection = prediction.TamponadeDetection()
                predictOutput = tamponadeDetection.predict(image)  # New method to handle in-memory images
                return jsonify(predictOutput)

        except Exception as error:
            app.logger.error(f"Error in processing request: {error}")
            return {'error': str(error)}, 500

api.add_resource(Test, '/')
api.add_resource(GetPredictionOutput, '/getPredictionOutput')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
