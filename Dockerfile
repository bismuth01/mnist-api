FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN mkdir -p ./models/CNN-MNIST/ ./models/mnist-resnet50/
RUN python -m venv /app/venv

COPY main.py ./main.py
COPY ./models/CNN-MNIST/CNN-mnist.h5 ./models/CNN-MNIST/CNN-mnist.h5
COPY ./models/mnist-resnet50/MNISTResNet50.h5 ./models/mnist-resnet50/MNISTResNet50.h5

COPY requirements.txt ./requirements.txt

SHELL ["/bin/bash", "-c"]
RUN source /app/venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8000

EXPOSE $PORT

CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port $PORT"]
