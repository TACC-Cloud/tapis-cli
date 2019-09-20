#!/bin/bash

docker build -t tacc/tapis-cli-ng:latest .

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker push tacc/tapis-cli-ng:latest
