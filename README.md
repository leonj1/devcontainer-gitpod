# DevContainer to Gitpod Converter

![DevContainer to Gitpod Converter](devcontainer_to_gitpod.jpg)

A web service that automatically converts DevContainer JSON configurations to Gitpod YAML configurations. This tool helps developers migrate their development environments from DevContainer to Gitpod with minimal effort.

## Features

- Converts DevContainer JSON to Gitpod YAML format
- RESTful API endpoint for conversion
- Web interface for easy access
- Docker containerization for consistent deployment

## Building and Running

### Prerequisites

- Python 3.7+
- Docker
- make (optional, for using Makefile commands)

### Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the containers:
   ```bash
   make build
   ```

3. Run the service:
   ```bash
   make run
   ```

The service will be available at:
- Web UI: http://localhost:4341
- API: http://localhost:4343

### Development Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Available Make Commands

- `make build` - Build the Docker containers
- `make run` - Start the service
- `make stop` - Stop the service
- `make restart` - Restart the service
- `make test` - Run the Python tests

## API Documentation

The API endpoint is available at `/convert` and accepts POST requests with a DevContainer JSON configuration in the request body.

Example request:
```bash
curl -X POST http://localhost:4343/convert \
  -H "Content-Type: application/json" \
  -d '{"name": "Python 3", "build": {"dockerfile": "Dockerfile"}}'
```
