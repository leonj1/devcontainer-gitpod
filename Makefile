.PHONY: build run stop restart

CONTAINER_NAME=devcontainer-converter
PORT=4343

# Default target
build:
	docker build -t $(CONTAINER_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8000 $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

restart: stop run
