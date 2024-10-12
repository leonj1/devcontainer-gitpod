# DevContainer to Gitpod Converter

This application converts DevContainer JSON configurations to Gitpod YAML configurations.

## Prerequisites

- Python 3.7+
- pip
- make (optional, for using Makefile commands)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Building and Running

You can use the provided Makefile commands or run the commands directly.

### Using Makefile

To start the server:
```
make stop build run
```

