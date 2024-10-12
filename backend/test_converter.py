import unittest
from converter import convert_devcontainer_to_gitpod
import json

class TestConverter(unittest.TestCase):
    def test_convert_devcontainer_to_gitpod(self):
        # Sample devcontainer.json input
        devcontainer_json = {
            "image": "mcr.microsoft.com/devcontainers/python:0-3.9",
            "features": {
                "ghcr.io/devcontainers/features/node:1": {"version": "lts"},
                "ghcr.io/devcontainers/features/git:1": {"version": "latest"}
            },
            "customizations": {
                "vscode": {
                    "settings": {"python.linting.enabled": True},
                    "extensions": ["ms-python.python", "ms-python.vscode-pylance"]
                }
            },
            "containerEnv": {
                "MY_ENV_VAR": "my_value"
            },
            "postCreateCommand": "pip install -r requirements.txt"
        }

        # Expected Gitpod YAML output
        expected_output = {
            "image": "mcr.microsoft.com/devcontainers/python:0-3.9",
            "tasks": [
                {
                    "name": "Install ghcr.io/devcontainers/features/node:1",
                    "command": "sudo apt-get update && sudo apt-get install -y ghcr.io/devcontainers/features/node:1=lts"
                },
                {
                    "name": "Install ghcr.io/devcontainers/features/git:1",
                    "command": "sudo apt-get update && sudo apt-get install -y ghcr.io/devcontainers/features/git:1=latest"
                },
                {
                    "env": {
                        "MY_ENV_VAR": "my_value"
                    }
                },
                {
                    "name": "Post-create command",
                    "command": "pip install -r requirements.txt"
                }
            ],
            "vscode": {
                "extensions": ["ms-python.python", "ms-python.vscode-pylance"],
                "settings": {"# Note": "VS Code settings should be configured separately in Gitpod"}
            }
        }

        # Convert devcontainer.json to Gitpod YAML
        result = convert_devcontainer_to_gitpod(devcontainer_json)

        # Compare the result with the expected output
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
