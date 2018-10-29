FROM python:3.4
ENV PYTHONUNBUFFERED 1

# Install packages for postgres, python dev for some project packages, and rsync for some fabric commands:
RUN apt-get update && \
  apt-get install -y \
    binutils \
    postgresql-client \
    rsync \
    gdal-bin

# Fabric for deploys:
RUN pip install -U pip
RUN pip install PyYAML fabric3 paramiko pycrypto ecdsa

RUN mkdir /code
WORKDIR /code

ADD requirements /code/requirements
RUN pip install -r requirements/dev.txt
