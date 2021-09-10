FROM index.docker.io/python:3.7

ARG CLI_VERSION=latest
ARG CLI_BRANCH=main
ARG PYTHON_PIP_VERSION=20.1.1
ARG PYTHON_VIRTUALENV_VERSION=16.7.0

LABEL org.label-schema.vendor = "Texas Advanced Computing Center"
LABEL org.label-schema.name = "TACC Tapis CLI Base"
LABEL org.label-schema.vcs-url = "https://github.com/TACC-Cloud/tapis-cli"
LABEL org.label-schema.organization=tacc.cloud
LABEL cloud.tacc.project="Tapis CLI"

# In-container volume mounts
# (For containers launched using TACC.cloud SSO identity)
ARG CORRAL=/corral
ARG STOCKYARD=/work

# Dependencies
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
    apt-utils bash curl dialog git vim rsync locales locales-all \
    build-essential autoconf libtool pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# jq for parsing JSON
RUN curl -L -sk -o /usr/local/bin/jq "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64" \
    && chmod a+x /usr/local/bin/jq

# Python 3
# RUN apt-get -y update && \
#     apt-get -y install --no-install-recommends \
#     python3 \
#     python3-dev \
#     python3-pip \
#     python3-setuptools && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Make python3 the default user python
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN pip3 install --quiet --upgrade pip==${PYTHON_PIP_VERSION}
RUN pip3 install --quiet --upgrade virtualenv==${PYTHON_VIRTUALENV_VERSION}

RUN mkdir -p /home
RUN mkdir -p /work
RUN mkdir -p /install

# Make pip behave better
COPY docker/pip.conf /etc/pip.conf

COPY . /install
WORKDIR /install
RUN pip install -q --upgrade tapis-cli

ENV TAPIS_CACHE_DIR=/root/.agave
ENV AGAVE_CACHE_DIR=/root/.agave
ENV TAPIS_CLI_VERSION=$CLI_VERSION

# Set command prompt
COPY 'docker/.dockerprompt' /home/.dockerprompt

RUN echo 'source /home/.dockerprompt' >> /root/.bashrc

RUN touch /root/.env && chmod u+rw /root/.env

CMD ["/bin/bash"]

WORKDIR /work
