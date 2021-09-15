FROM python:3.9-slim-buster

LABEL maintainer="Julien Alardot <alardotj.pro@@gmail.com>"

WORKDIR /usr/src/app
#RUN export FLASK_APP=none

RUN apt-get update -y
#RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

EXPOSE 5000
COPY . .
CMD [ "streamlit","run", "./app/app.py" ]
