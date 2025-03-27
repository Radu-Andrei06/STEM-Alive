
import pytest
from ai.generators.text_generator import get_ai_response, ai_to_json
from unittest.mock import MagicMock, patch
import json

class TestGetAIResponse:
    @pytest.mark.usefixtures("mock_gemini_client")
    def test_successful_response(self, mock_gemini_client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = "Mock AI response"
        mock_gemini_client.return_value = mock_response

        # Call the function
        result = get_ai_response(
            prompt="Test prompt",
            model="gemini-1.5-flash",  # Use a valid model name
            config="Test config",
            name="Test Name"
        )

        # Verify results
        assert result == "Mock AI response"
        mock_gemini_client.assert_called_once()

    @pytest.mark.usefixtures("mock_gemini_client")
    def test_error_handling(self, mock_gemini_client):
        # Setup mock to raise error
        mock_gemini_client.side_effect = Exception("API Error")

        # Verify error is raised
        with pytest.raises(Exception) as exc_info:
            get_ai_response(
                prompt="Test prompt",
                model="gemini-1.5-flash",
                config="Test config",
                name="Test Name"
            )

        assert "API Error" in str(exc_info.value)


class TestAIToJSON:
    @patch('ai.generators.text_generator.get_ai_response')
    def test_successful_json_output(self, mock_get_response):
        mock_get_response.return_value = "Test response"
        result = ai_to_json(
            prompt="Test prompt",
            model="gemini-1.5-flash",
            config="Test config",
            name="Test Name"
        )
        data = json.loads(result)
        assert data["name"] == "Test Name"
        assert data["response"] == "Test response"
        assert data["settings"]["prompt"] == "Test prompt"

    @patch('ai.generators.text_generator.get_ai_response')
    def test_error_json_output(self, mock_get_response):
        mock_get_response.side_effect = Exception("Test error")
        result = ai_to_json(
            prompt="Test prompt",
            model="gemini-1.5-flash",
            config="Test config",
            name="Test Name"
        )
        data = json.loads(result)
        assert data["name"] == "Test Name"
        assert "Error" in data["response"]
        assert "Test error" in data["response"]