#!/bin/bash

docker build -t tacc/tapis-cli:latest .

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker push tacc/tapis-cli:latest
