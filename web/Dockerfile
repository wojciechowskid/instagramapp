FROM python:3.7-slim

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

COPY . .
