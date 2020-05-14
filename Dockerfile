FROM python:3
WORKDIR /code

RUN apt update
RUN apt install -y x11-utils tesseract-ocr tesseract-ocr-jpn libtesseract-dev scrot xdotool

COPY requirements.txt /code/
RUN pip install -r requirements.txt
