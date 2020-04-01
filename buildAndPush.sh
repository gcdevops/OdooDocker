#!/bin/bash
DOCKER_TAG=$1
docker build -t odoobentest:$DOCKER_TAG .
docker tag odoobentest:$DOCKER_TAG mtscontainers.azurecr.io/odoobentest:$DOCKER_TAG
az acr login --name mtscontainers
docker push mtscontainers.azurecr.io/odoobentest:$DOCKER_TAG