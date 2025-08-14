import os
import pytest
from unittest.mock import Mock, mock_open, patch
from managers import CustomizationManager
from utils import FilePath


@pytest.fixture()
def customization_manager():
    pathfinder = Mock(spec=FilePath)
    pathfinder.get_custom_text.return_value = "fakefile.txt"
    return CustomizationManager(pathfinder)


@pytest.fixture()
def base_path():
    return os.path.dirname(__file__)


def test_get_site(customization_manager, base_path):
    fake_file_content = "SMF9"

    with patch("builtins.open", mock_open(read_data=fake_file_content)):
        result = customization_manager.get_site(base_path)
        assert result == "SMF9"


def test_get_shifts(customization_manager, base_path):
    fake_file_content = "04-00-00\n09-30-00"

    with patch("builtins.open", mock_open(read_data=fake_file_content)):
        result = customization_manager.get_shifts(base_path)
        assert result == "04-00-00\n09-30-00"


def test_get_roles(customization_manager, base_path):
    fake_file_content = "End of Line\nProblem Solve\nAudit"

    with patch("builtins.open", mock_open(read_data=fake_file_content)):
        result = customization_manager.get_roles(base_path)
        assert result == "End of Line\nProblem Solve\nAudit"
