FROM python:3.11-bullseye

COPY . /beringlab
WORKDIR /beringlab

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

ENTRYPOINT python manage.py migrate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell && uvicorn beringlab.asgi:application --host 0.0.0.0 --port 8888
