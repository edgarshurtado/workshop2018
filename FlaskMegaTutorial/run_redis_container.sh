#!/usr/bin/env bash
REDIS_CONTAINER_NAME=redis_edgar_c
docker stop ${REDIS_CONTAINER_NAME}
docker rm ${REDIS_CONTAINER_NAME}

docker run -d -p 6379:6379 --name ${REDIS_CONTAINER_NAME} redis
