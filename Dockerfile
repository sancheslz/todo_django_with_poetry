FROM python:3.12

ARG PROJECT_NAME \
    ENVIRONMENT \
    PORT \
    DOCKER_PORT \
    VOLUME_DOCKER

ENV PROJECT_NAME=${PROJECT_NAME} \
    ENVIRONMENT=${ENVIRONMENT} \
    PORT=${PORT} \
    DOCKER_PORT=${DOCKER_PORT} \
    VOLUME_DOCKER=${VOLUME_DOCKER} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
        build-essential \ 
        libpq-dev \ 
        curl \ 
        postgresql-client \ 
        && \
        rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install poetry

WORKDIR /app

COPY . .

RUN chmod u+x entrypoint.sh

WORKDIR /app/$PROJECT_NAME/

COPY ${PROJECT_NAME}/*.toml .

RUN if [ -f "pyproject.toml" ]; then poetry install; fi

EXPOSE $PORT

ENTRYPOINT [ "./entrypoint.sh" ]
