# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /proctoring

COPY ./flask-backend/ .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt


ENTRYPOINT [ "python" ]
CMD ["app.py"]