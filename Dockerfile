FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY main.py ./main.py
COPY ./models ./models
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8000

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
