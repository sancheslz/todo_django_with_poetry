include .env
export


image:
	docker rm -f $(shell docker ps -a -q) || true \
	&& docker build -t image_${PROJECT_NAME} .

container:
	docker rm -f $(shell docker ps -a -q) || true \
	&& docker run \
		--env-file .env \
		--publish 8000:8000 \
		--volume "$(shell pwd):/app" \
		--name back_${PROJECT_NAME} \
		image_${PROJECT_NAME}

build: image container

bash:
	docker exec -it -w /app/${PROJECT_NAME} back_${PROJECT_NAME} bash

manage:
	echo "$(MAKECMDGOALS)"
	docker exec -it \
		-w /app/${PROJECT_NAME} \
		back_${PROJECT_NAME} \
		poetry run python manage.py \
		$(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

makemigrations:
	docker exec -w /app/${PROJECT_NAME} \
		back_${PROJECT_NAME} \
		poetry run python manage.py makemigrations

migrate:
	docker exec -w /app/${PROJECT_NAME} \
		back_${PROJECT_NAME} \
		poetry run python manage.py migrate

server:
	docker exec -w /app/${PROJECT_NAME} \
		back_${PROJECT_NAME} \
		poetry run python manage.py runserver

start:
	docker start back_${PROJECT_NAME}

stop:
	docker stop back_${PROJECT_NAME}

test:
	docker exec -w /app/${PROJECT_NAME} \
		back_${PROJECT_NAME} \
		poetry run pytest
