import os
import tempfile
import builtins
import pytest
import tkinter as tk
from unittest.mock import Mock, mock_open, patch
from managers import PermissionsManager
from utils import FilePath


@pytest.fixture()
def permissions_manager():
    pathfinder = Mock(spec=FilePath())
    pathfinder.get_custom_text.return_value = "fakefile.txt"
    pathfinder.get_permissions.return_value = "fakefile.txt"
    return PermissionsManager(pathfinder)


@pytest.fixture()
def text_box():
    root = tk.Tk()
    root.withdraw()
    root.title("Test")
    text_box = tk.Text(root)

    yield text_box
    root.update_idletasks()  # helps with clean shutdown, occasional failures may still persist
    root.destroy()


@pytest.fixture()
def base_path():
    return os.path.dirname(__file__)


def test_check_permissions(permissions_manager, base_path):
    fake_file_content = "fake permissions"

    with patch("managers.permissions_manager.open", mock_open(read_data=fake_file_content)):
        result = permissions_manager.check_permissions(base_path)
        assert result == "fake permissions"


def test_get_saved_roles(permissions_manager, base_path):
    fake_file_content = "End of Line\nProblem Solve\nAudit"

    with patch("managers.permissions_manager.open", mock_open(read_data=fake_file_content)):
        result = permissions_manager.get_saved_roles(base_path)
        assert result == ["End of Line", "Problem Solve", "Audit"]


@pytest.mark.parametrize("role",
                         [
                             ("End of Line",),
                             ("Problem Solve",),
                             ("Audit",)
                         ])
def test_get_permissions_string(permissions_manager, role, base_path):
    fake_file_content = "## End of Line"

    with patch("managers.permissions_manager.open", mock_open(read_data=fake_file_content)):
        result = permissions_manager.get_permissions_string(role, base_path)
        assert result[:2] == "##"  # Permissions strings should start with hashtags


@pytest.mark.parametrize("chars, indirect_roles",
                         [
                             ("## End of Line\n\ngalleaus\n\n", ["End of Line"]),
                             ("## Problem Solve\n\ngalleaus\n\n", ["Problem Solve"]),
                             ("## Problem Solve\n\ngalleaus\n\n## End of Line\n\ngalleaus\n\n",
                              ["Problem Solve", "End of Line"])
                         ])
def test_check_edited_permissions(permissions_manager, text_box, chars, indirect_roles):
    text_box.insert(tk.END, chars=chars)
    result = permissions_manager.check_edited_permissions(text_box, indirect_roles)
    for permission in result:
        assert permission.startswith("##")


def test_save_permissions(permissions_manager, base_path, text_box):
    fake_file_content = "End of Line"
    new_content = "## End of Line\n\ngalleaus\n\n"
    text_box.insert(tk.END, chars=new_content)

    with tempfile.NamedTemporaryFile(mode="w+t") as temp:
        temp_path = temp.name
        permissions_manager.pathfinder.get_permissions.return_value = temp_path
        read_mock = mock_open(read_data=fake_file_content)
        real_open = builtins.open

        def selective_open(filename, mode="r", *args, **kwargs):
            if filename == "fakefile.txt" and mode == "r":
                return read_mock(filename, mode, *args, **kwargs)
            else:
                return real_open(filename, mode, *args, **kwargs)

        with patch("managers.permissions_manager.open", side_effect=selective_open):
            result = permissions_manager.save_permissions(base_path, text_box)

            assert result

        with open(temp_path) as file:
            content = file.read()
            assert content == new_content
