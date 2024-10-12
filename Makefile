.PHONY: build run stop restart

API_CONTAINER_NAME=devcontainer-converter-api
API_PORT=4343
WEB_CONTAINER_NAME=devcontainer-converter-web
WEB_PORT=4341

# Default target
build:
	docker build -t $(API_CONTAINER_NAME) .
	cd frontend && docker build -t $(WEB_CONTAINER_NAME) .

run:
	docker run -d --name $(API_CONTAINER_NAME) -p $(API_PORT):8000 $(API_CONTAINER_NAME)
	docker run -d --name $(WEB_CONTAINER_NAME) -p $(WEB_PORT):8000 $(WEB_CONTAINER_NAME)

stop:
	docker stop $(API_CONTAINER_NAME) || true
	docker rm $(API_CONTAINER_NAME) || true
	docker stop $(WEB_CONTAINER_NAME) || true
	docker rm $(WEB_CONTAINER_NAME) || true

restart: stop run
