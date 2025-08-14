from utils.interfaces import CustomizationManagerInterface, FilePathInterface


class CustomizationManager(CustomizationManagerInterface):
    def __init__(self, pathfinder: FilePathInterface):
        self.pathfinder = pathfinder

    def get_site(self, base_path):
        """Opens site.txt and returns site ID"""
        with open(self.pathfinder.get_custom_text(base_path, "site"), "r") as file:
            site = file.read()
            return site

    def get_shifts(self, base_path):
        """Opens saved_shifts.txt and returns all shifts"""
        with open(self.pathfinder.get_custom_text(base_path, "saved_shifts"), "r") as file:
            shifts = file.read()
            return shifts

    def get_roles(self, base_path):
        """Opens saved_roles.txt and returns all roles"""
        with open(self.pathfinder.get_custom_text(base_path, "saved_roles"), "r") as file:
            text = file.read()
            return text

    def save(self, filename, text, base_path):
        """Writes text in files for given filename and text arguments"""
        with open(self.pathfinder.get_custom_text(base_path, filename), "w") as file:
            for line in text:
                file.write(line + "\n")
