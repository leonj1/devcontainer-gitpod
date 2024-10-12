.PHONY: build run stop

CONTAINER_NAME=devcontainer-converter-web
PORT=3000

build:
	docker build -t $(CONTAINER_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):3000 $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
