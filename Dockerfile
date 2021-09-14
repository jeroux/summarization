FROM python:3.9-slim-buster

LABEL maintainer=["Julien Alardot <alardotj.pro@@gmail.com>", ]

WORKDIR /usr/src/app
#RUN export FLASK_APP=none

RUN apt-get update -y
#RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
#RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

EXPOSE 5000
COPY . .
CMD [ "python", "./app/app.py" ]