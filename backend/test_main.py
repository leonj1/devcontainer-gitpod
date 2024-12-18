import pytest
from fastapi.testclient import TestClient
from main import app
import logging

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