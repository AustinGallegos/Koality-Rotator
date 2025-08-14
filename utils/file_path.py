import os
import sys
from .interfaces import FilePathInterface


class FilePath(FilePathInterface):
    def get_paths(self):
        """Determine temporary and base paths depending on whether
        the app is frozen or running in development."""
        if getattr(sys, "frozen", False):  # If app is running as .exe file
            current_user = os.getlogin()
            temp_path = sys._MEIPASS  # noqa: Eprotected
            base_path = f"C:\\Users\\{current_user}\\.config\\Koality Rotator"
        else:  # If app is running in Pycharm
            temp_path = None
            base_path = os.path.dirname(os.path.dirname(__file__))
        return temp_path, base_path

    def app_init(self, temp_path, base_path):
        """Gets filepath for specific role permissions depending on whether the app is frozen or running in a normal
            Python environment"""
        if temp_path:  # Execute function only if app is running as .exe file
            file_path = os.path.join(base_path, "txt")
            os.makedirs(file_path, exist_ok=True)

            files = [
                "End of Line.txt", "Problem Solve.txt", "Waterspider.txt", "Refurb.txt", "Unload.txt",
                "Detrash.txt", "saved_roles.txt", "saved_shifts.txt", "site.txt"
            ]

            for filename in files:
                self.create_file(temp_path, file_path, filename)

    def create_file(self, temp_path, file_path, filename):
        """Create a file at the target path by copying it from a
        temporary location if it doesn’t exist."""
        full_path = os.path.join(file_path, filename)
        full_temp_path = os.path.join(temp_path, "txt", filename)

        if not os.path.exists(full_path):
            with open(full_temp_path) as file2:
                text = file2.read()
            with open(full_path, "w") as file:
                file.write(text)

    def get_permissions(self, role, base_path):
        """Gets filepath for specific role permissions. Creates it if it doesn't exist."""
        file_path = os.path.join(base_path, "txt", f"{role}.txt")
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(f"## {role} Permissions {"-" * 30}\nEnter Logins Here\n\n")
        return file_path

    def get_custom_text(self, base_path, file):
        """Gets filepath for custom files such as saved_roles, saved_shifts, or site ID."""
        file_path = os.path.join(base_path, "txt", f"{file}.txt")
        return file_path

    def get_image_path(self, temp_path, base_path, filename):
        """Gets filepath for Amazon Smile Logo depending on whether the app is frozen or running in a normal Python
        Environment"""
        if temp_path:  # running as .exe file
            image_path = os.path.join(temp_path, "images", filename)
        else:  # running in pycharm
            image_path = os.path.join(base_path, "images", filename)
        return image_path
