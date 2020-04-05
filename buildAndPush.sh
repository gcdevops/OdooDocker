#!/bin/bash
DOCKER_TAG=$1
docker build -t odoo:$DOCKER_TAG . --no-cache
docker tag odoo:$DOCKER_TAG mtscontainers.azurecr.io/hrm-odoo:$DOCKER_TAG
az acr login --name mtscontainers
docker push mtscontainers.azurecr.io/odoo:$DOCKER_TAG