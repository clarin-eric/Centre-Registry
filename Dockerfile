# pull official base image
FROM python:3.12.1-alpine3.19

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . .
RUN pip install requests pandas
RUN pip install ./centre-registry-app
COPY ./Centre-Registry-config .
RUN pip install ./Centre-Registry-config

# copy project
COPY . .
