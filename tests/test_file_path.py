import os
import sys
import pytest
import tempfile
from utils import FilePath


@pytest.fixture()
def file_path():
    pathfinder = FilePath()
    return pathfinder


def test_get_paths_frozen(file_path, monkeypatch):
    sys.frozen = True
    sys._MEIPASS = "C:\\Temp\\meipass"
    monkeypatch.setattr(os, "getlogin", lambda: "testuser")

    expected_temp_path = "C:\\Temp\\meipass"
    expected_base_path = "C:\\Users\\testuser\\.config\\Koality Rotator"
    temp_path, base_path = file_path.get_paths()

    assert temp_path == expected_temp_path
    assert base_path == expected_base_path

    delattr(sys, "frozen")
    delattr(sys, "_MEIPASS")


def test_get_paths_not_frozen(file_path):
    expected_temp_path = None
    expected_base_path = os.path.dirname(os.path.dirname(__file__))
    temp_path, base_path = file_path.get_paths()

    assert temp_path == expected_temp_path
    assert base_path == expected_base_path


def test_app_init(file_path):
    with tempfile.TemporaryDirectory() as temp_path:
        temp_dir = os.path.join(temp_path, "txt")
        os.makedirs(temp_dir)

        file_names = [
            "End of Line.txt", "Problem Solve.txt", "Waterspider.txt", "Refurb.txt", "Unload.txt",
            "Detrash.txt", "saved_roles.txt", "saved_shifts.txt", "site.txt"
        ]
        for filename in file_names:
            with open(os.path.join(temp_dir, filename), "w") as file:
                file.write("fake content")

        with tempfile.TemporaryDirectory() as base_path:
            file_path.app_init(temp_path, base_path)  # call file_path's method

            base_dir = os.path.join(base_path, "txt")
            for filename in file_names:
                file = os.path.join(base_dir, filename)
                assert os.path.exists(file)

                with open(file) as result:
                    content = result.read()
                    expected = "fake content"
                    assert content == expected


@pytest.mark.parametrize(
    "role", [
        ("End of Line",),
        ("Problem Solve",),
        ("Audit",)
    ]
)
def test_get_permissions(file_path, role):
    with tempfile.TemporaryDirectory() as base_path:
        base_dir = os.path.join(base_path, "txt")
        os.makedirs(base_dir)

        file_path.get_permissions(role, base_path)  # call file_path's method

        result_path = os.path.join(base_path, "txt", f"{role}.txt")
        with open(result_path) as result:
            content = result.read()
            expected = f"## {role} Permissions {"-" * 30}\nEnter Logins Here\n\n"
            assert content == expected


def test_get_custom_text(file_path):
    fake_path = "fake path"
    fake_file = "fake file"
    result = file_path.get_custom_text(fake_path, fake_file)
    expected = os.path.join(fake_path, "txt", f"{fake_file}.txt")
    assert result == expected


def get_image_path(file_path):
    fake_temp_path = "fake temp path"
    fake_base_path = "fake base path"
    fake_file = "fake file"

    result1 = file_path.get_image_path(fake_temp_path, None, fake_file)
    expected1 = os.path.join(fake_temp_path, "images", fake_file)
    assert result1 == expected1

    result2 = file_path.get_image_path(None, fake_base_path, fake_file)
    expected2 = os.path.join(fake_base_path, "images", fake_file)
    assert result2 == expected2

    result3 = file_path.get_image_path(fake_temp_path, fake_base_path, fake_file)
    assert result3 == expected1
