FROM python:3.6

MAINTAINER Maciej Januszewski <maciek@mjanuszewski.pl>

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    postgresql-contrib \
    build-essential \
    checkinstall \
    vim && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /code/

RUN chmod +x *.sh