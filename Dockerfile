FROM python:3.9-slim-buster

LABEL maintainer="Julien Alardot <alardotj.pro@@gmail.com>"

EXPOSE 8501
WORKDIR /usr/src/app
#RUN export FLASK_APP=none

RUN apt-get update -y
#RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./
COPY ./app/DockerPreLoadModels.py ./app/DockerPreLoadModels.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python ./app/DockerPreLoadModels.py
COPY . .
CMD [ "streamlit","run", "./app/app.py" ]
