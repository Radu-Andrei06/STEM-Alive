
import pytest
from unittest.mock import MagicMock, patch
from ai.generators.text_generator import client

@pytest.fixture
def mock_gemini_client():
    """Fixture to mock the Gemini client generate_content method"""
    with patch.object(client.models, 'generate_content') as mock_generate:
        yield mock_generate
