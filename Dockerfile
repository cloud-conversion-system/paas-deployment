FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y redis-server

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD service redis-server start && celery -A cloud_conversion_tool.celery_script worker -l info & \
    cd cloud_conversion_tool && python3 -m flask run --host=0.0.0.0 -p 80
