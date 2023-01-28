FROM python:3.11-bullseye

COPY . /beringlab
WORKDIR /beringlab

RUN pip install -r requirements.txt

ENTRYPOINT python manage.py migrate && uvicorn beringlab.asgi:application --host 0.0.0.0 --port 8888
