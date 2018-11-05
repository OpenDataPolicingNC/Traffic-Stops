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

# nvm environment variables
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR
ENV NODE_VERSION 6.14.4

# install nvm
# https://github.com/creationix/nvm#install-script
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

# install node and npm
RUN . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# confirm installation
RUN node -v
RUN npm -v

RUN npm install -g gulp
