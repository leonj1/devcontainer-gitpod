import pytest
from fastapi.testclient import TestClient
from main import app
import logging
import yaml

client = TestClient(app)

class TestConvertToGitpod:
    def test_convert_to_gitpod_success(self, mocker):
        # Mock the convert_devcontainer_to_gitpod function
        mock_convert = mocker.patch('main.convert_devcontainer_to_gitpod')
        mock_convert.return_value = {'workspace': 'test'}

        devcontainer_json = {"name": "test"}
        response = client.post("/convert", json=devcontainer_json)

        assert response.status_code == 200
        assert response.text == "workspace: test\n"

    def test_convert_to_gitpod_invalid_input(self, mocker):
        # Mock the convert_devcontainer_to_gitpod function to raise an exception
        mock_convert = mocker.patch('main.convert_devcontainer_to_gitpod')
        mock_convert.side_effect = Exception("Invalid input")

        # Send valid JSON that will trigger the converter error
        devcontainer_json = {"name": "test"}
        response = client.post("/convert", json=devcontainer_json)

        assert response.status_code == 500
        assert response.json() == {"detail": "Invalid input"}

    def test_convert_to_gitpod_logging(self, mocker):
        # Mock the logger
        mock_logger = mocker.patch('main.logger')

        devcontainer_json = {"name": "test"}
        client.post("/convert", json=devcontainer_json)

        # Check if the logger was called with expected messages
        mock_logger.info.assert_any_call("Received request to convert devcontainer to Gitpod config")
        mock_logger.info.assert_any_call("Converting devcontainer JSON to Gitpod YAML")
        mock_logger.info.assert_any_call("Converting Gitpod config to YAML string")
        mock_logger.info.assert_any_call("Conversion completed successfully")

    def test_convert_to_gitpod_invalid_json(self):
        test_cases = [
            ("Empty request", "", "value_error.missing"),
            ("Invalid JSON syntax", "{invalid}", "value_error.jsondecode"),
            ("Array instead of object", "[]", "value_error.missing"),
            ("Missing required field", '{}', "value_error.missing"),
            ("Wrong field type", '{"name": []}', "type_error.str"),
        ]

        for test_name, payload, expected_error in test_cases:
            response = client.post(
                "/convert", 
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 422, f"{test_name} should return 422"
            error_detail = response.json()["detail"]
            assert isinstance(error_detail, list), f"{test_name} should return validation errors"
            error_types = [err.get("type", "") for err in error_detail]
            assert expected_error in error_types, f"{test_name} should have error type {expected_error}"

def test_convert_complex_devcontainer():
    """Test conversion of a complex devcontainer with env vars and extensions."""
    devcontainer_json = {
        "image": "mcr.microsoft.com/devcontainers/typescript-node",
        "customizations": {
            "vscode": {
                "extensions": [
                    "streetsidesoftware.code-spell-checker"
                ]
            }
        },
        "forwardPorts": [3000],
        "containerEnv": {
            "MY_CONTAINER_VAR": "some-value-here",
            "MY_CONTAINER_VAR2": "${localEnv:SOME_LOCAL_VAR}"
        },
        "remoteEnv": {
            "PATH": "${containerEnv:PATH}:/some/other/path",
            "MY_REMOTE_VARIABLE": "some-other-value-here",
            "MY_REMOTE_VARIABLE2": "${localEnv:SOME_LOCAL_VAR}"
        }
    }

    response = client.post("/convert", json=devcontainer_json)
    assert response.status_code == 200
    
    # Parse the YAML response to validate structure
    gitpod_yaml = yaml.safe_load(response.text)
    
    # Validate image
    assert gitpod_yaml["image"] == devcontainer_json["image"]
    
    # Validate ports
    assert gitpod_yaml["ports"] == [{"port": 3000}]
    
    # Validate VS Code extensions
    assert "vscode" in gitpod_yaml
    assert gitpod_yaml["vscode"]["extensions"] == ["streetsidesoftware.code-spell-checker"]
    
    # Validate environment variables
    assert "env" in gitpod_yaml
    expected_env = {
        "MY_CONTAINER_VAR": "some-value-here",
        "MY_CONTAINER_VAR2": "${SOME_LOCAL_VAR}",  # localEnv prefix is removed
        "PATH": "${PATH}:/some/other/path",  # containerEnv is simplified
        "MY_REMOTE_VARIABLE": "some-other-value-here",
        "MY_REMOTE_VARIABLE2": "${SOME_LOCAL_VAR}"  # localEnv prefix is removed
    }
    assert gitpod_yaml["env"] == expected_env

def test_invalid_json_error():
    """Test that invalid JSON returns a 422 with detailed error information."""
    # Test case 1: Invalid JSON with missing quotes
    invalid_json = """{
    "image": mcr.microsoft.com/devcontainers/typescript-node,
    "customizations": {
        "vscode": {
            "extensions": [
                "streetsidesoftware.code-spell-checker"
            ]
        }
    }
}"""

    response = client.post("/convert", content=invalid_json)
    assert response.status_code == 422
    
    error_detail = response.json()
    assert error_detail["error"] == "Invalid JSON format"
    assert "message" in error_detail
    assert error_detail["line_number"] > 0  # Should have line number
    assert error_detail["column"] > 0  # Should have column number
    assert "context" in error_detail  # Should show the problematic line
    assert "mcr.microsoft.com" in error_detail["context"]  # Should show the unquoted string
    
    # Test case 2: Invalid JSON with unterminated string
    response = client.post("/convert", content='{"key": "missing quote}')
    assert response.status_code == 422
    error_detail = response.json()
    assert error_detail["error"] == "Invalid JSON format"
    assert "Unterminated string" in error_detail["message"]
    
    # Test case 3: Empty input
    response = client.post("/convert", content="")
    assert response.status_code == 422
    error_detail = response.json()
    assert error_detail["error"] == "Invalid JSON format"
    assert error_detail["message"] == "Empty input"
    assert error_detail["context"] == "<empty>"