.PHONY: build run stop restart test

API_CONTAINER_NAME=devcontainer-converter-api
API_PORT=4343
API_HOST=devcontainer-api.joseserver.com
WEB_CONTAINER_NAME=devcontainer-converter-web
WEB_PORT=4341

export API_PORT
export API_HOST

# Default target
build:
	docker build -t $(API_CONTAINER_NAME) .
	cd frontend && docker build --build-arg API_PORT=$(API_PORT) --build-arg API_HOST=$(API_HOST) -t $(WEB_CONTAINER_NAME) .

run:
	docker run -d --name $(API_CONTAINER_NAME) -p $(API_PORT):8000 $(API_CONTAINER_NAME)
	docker run -d --name $(WEB_CONTAINER_NAME) -p $(WEB_PORT):3000 -e REACT_APP_API_HOST=$(API_HOST) -e REACT_APP_API_PORT=$(API_PORT) $(WEB_CONTAINER_NAME)

stop:
	docker stop $(API_CONTAINER_NAME) || true
	docker rm $(API_CONTAINER_NAME) || true
	docker stop $(WEB_CONTAINER_NAME) || true
	docker rm $(WEB_CONTAINER_NAME) || true

restart: stop run

test:
	cd backend && $ docker run --rm devcontainer-gitpod-test
