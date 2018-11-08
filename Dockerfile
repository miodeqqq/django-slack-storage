FROM python:3.6.6

MAINTAINER Maciej Januszewski <maciek@mjanuszewski.pl>

ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /src

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    python3-software-properties \
    ca-certificates \
    build-essential \
    libffi-dev \
    libssl-dev \
    dbus-x11 \
    postgresql \
    openssl \
    python-openssl \
    wireless-tools \
    python-pypdf2 \
    vim && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /src

RUN chmod +x *.py
RUN chmod +x *.sh