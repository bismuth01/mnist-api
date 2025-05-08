# MNIST API

Contains code to query 2 models trained on the MNIST dataset to classify between handwritten digits.
The types of models are : ResNet50 and CNN.

## Installation

### Using docker image
Pull the docker image using `docker pull b1smuth/mnist-api:2.1`.

To run the image using `docker run -p 8000:8000 b1smuth/mnist-api:2.1` to expose port 8000 using port 8000 of the machine.

### Using source code
First clone the repository with all the submodules

`git clone --recurse-submodules https://github.com/bismuth01/mnist-api.git`

This might take a while since the .h5 files are large.
In the root directory of the repository, install all necessary pip packages by using the command
`pip install -r requirements.txt`

Also install tensorflow since it is not inside the `requirements.txt` due to usage of Tensorflow 2.19 Docker image.
`pip install tensorflow`

Then to start the API server
`fastapi dev main.py`

## How to use
The API runs on port `8000` by default.
To check if it's running, try a GET request on the `/status` endpoint.

Send a your image at `/predict_image` endpoint with key value `file` to get the prediction response.

## Sample response

```
{
    "ResNet":{
        "prediction":{
            "class": 9,
            "confidence":0.9368
            }
        },
    "CNN":{
        "prediction":{
            "class": 9,,
            "confidence"::0.9964
            }
        }
}
```

## How it works ?
The image draw on canvas is resized to a 28x28 pixels image and then fed into the models for prediction.
