import os
import shutil
import sys
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS
from wasteDetection.pipeline.training_pipeline import TrainPipeline
from wasteDetection.utils.main_utils import decodeImage, encodeImageIntoBase64
from wasteDetection.constant.application import APP_HOST, APP_PORT
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.constant.training_pipeline.config import set_data

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"


clApp = ClientApp()


@app.route('/train', methods=['POST'])
def trainRoute():
    try:
        data = request.json
        if 'data_link' not in data or 'epochs' not in data or 'batch_size' not in data:
            return Response("Missing 'data_link', 'epochs', or 'batch_size' in request", status=400)

        data_link = data['data_link']
        epochs = int(data['epochs'])
        batch_size = int(data['batch_size'])    
        set_data(epochs,batch_size)
        logging.info(f"Updated DATA_DOWNLOAD_URL to: {data_link}")
        logging.info(f"Training parameters - Epochs: {epochs}, Batch Size: {batch_size}")

        # Run the training pipeline
        pipeline = TrainPipeline(data_link)
        pipeline.run_pipeline()

        return jsonify({"message": "Training initiated successfully"}), 200

    except ValueError as ve:
        logging.error(f"Validation error: {str(ve)}")
        return Response(str(ve), status=400)
    except Exception as e:
        logging.error(f"Error during training: {str(e)}")
        return Response(str(e), status=500)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    print("server running",APP_PORT)
    app.run(host=APP_HOST, port=APP_PORT)
