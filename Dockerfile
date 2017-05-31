FROM python:3.6

MAINTAINER Maciej Januszewski <maciek@mjanuszewski.pl>

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-contrib

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/

RUN chmod +x *.sh