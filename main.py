import os
from typing import Union
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
import cv2
import asyncio
from fastapi import FastAPI, File, UploadFile
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

HOSTED_FRONTEND = os.environ.get('HOSTED_FRONTEND')
TESTING_FRONTEND = os.environ.get('TESTING_FRONTEND')

origins = [
    HOSTED_FRONTEND,
    TESTING_FRONTEND
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMG_SIZE = (28, 28)

resnet = load_model('./models/mnist-resnet50/MNISTResNet50.h5')
cnn = load_model('./models/CNN-MNIST/CNN-mnist.h5')

def preprocess_image(file_bytes: bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, IMG_SIZE) # Image size taken in by models
    image = image / 255.0 # Normalize image
    image = image.reshape((28, 28, 1))
    image = np.expand_dims(image, axis=0)

    return image

async def predict(img: np.ndarray, model: Model, model_type: str):
    prediction = model.predict(img)[0]
    class_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # ResNet is categorical while CNN and ANN are binary
    index = int(np.argmax(prediction))
    predicted_class = class_labels[index]
    confidence = float(prediction[index]) # convert to regular float for JSON serialization

    print(f"[LOG] Prediction from {model_type.upper()}: {prediction}")

    return {
        "class": predicted_class,
        "confidence": round(confidence, 4)
    }



@app.get("/status")
def read_root():
    return {"status": "Running"}

@app.post("/predict_image")
async def predict_image(file: UploadFile):
    file_bytes = await file.read()
    cnn_img_array = preprocess_image(file_bytes)
    resnet_img_array = preprocess_image(file_bytes)

    tasks = [
        predict(resnet_img_array, resnet, 'resnet'),
        predict(cnn_img_array, cnn, 'cnn')
    ]

    results = await asyncio.gather(*tasks)

    return {
        "ResNet": {"prediction": results[0]},
        "CNN": {"prediction": results[1]}
    }
