from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import prediction

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
            data = request.get_json()
            if not data:
                return {"error": "No data provided or invalid JSON"}, 400

            if not isinstance(data, dict):
                return {"error": "Invalid data format, expecting a JSON object"}, 400

            image_path = data.get("image_path")
            if not isinstance(image_path, str):
                return {"error": "Invalid image path, expecting a string"}, 400

            tamponadeDetection = prediction.TamponadeDetection()
            predictOutput = tamponadeDetection.predict(image_path)
            return jsonify(predictOutput)

        except Exception as error:
            app.logger.error(f"Error in processing request: {error}")
            return {'error': str(error)}, 500


api.add_resource(Test, '/')
api.add_resource(GetPredictionOutput, '/getPredictionOutput')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
