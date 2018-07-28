#!/usr/bin/env bash
REDIS_IMAGE_NAME=redis_edgar
REDIS_CONTAINER_NAME=redis_edgar_c
docker rm ${REDIS_CONTAINER_NAME}
docker rmi ${REDIS_IMAGE_NAME}

DOCKER_CONTEXT=.
REDIS_DOCKERFILE=./RedisDockerfile
docker build -t ${REDIS_IMAGE_NAME} -f ${REDIS_DOCKERFILE} ${DOCKER_CONTEXT}
docker run -d -p 6379:6379 --name ${REDIS_CONTAINER_NAME} ${REDIS_IMAGE_NAME}
