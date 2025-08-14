from utils.interfaces import PermissionsManagerInterface, FilePathInterface


class PermissionsManager(PermissionsManagerInterface):
    def __init__(self, pathfinder: FilePathInterface):
        self.pathfinder = pathfinder

    def check_permissions(self, base_path):
        """Reads permissions files on user's PC for each saved indirect role."""
        indirect_roles = self.get_saved_roles(base_path)

        permissions_string = ""

        for role in indirect_roles:
            text = self.get_permissions_string(role, base_path)
            permissions_string += text

        return permissions_string

    def get_saved_roles(self, base_path):
        """Retrieve a list of saved roles from a file."""
        with open(self.pathfinder.get_custom_text(base_path, "saved_roles"), "r") as file:
            return [line.strip() for line in file.readlines()]

    def get_permissions_string(self, role, base_path):
        """Get the permissions string for a specific role from a file."""
        with open(self.pathfinder.get_permissions(role, base_path), "r") as file:
            return file.read()

    def save_permissions(self, base_path, text_box):
        """Saves permissions files on user's PC for each saved indirect role."""
        indirect_roles = self.get_saved_roles(base_path)

        saved_permissions = self.check_edited_permissions(text_box, indirect_roles)

        if not saved_permissions:
            return False
        else:
            saved_permissions_iter = iter(saved_permissions)
            for role in indirect_roles:
                self.save_edited_permissions(role, base_path, saved_permissions_iter)
            return True

    def check_edited_permissions(self, text_box, indirect_roles):
        """Verify and format edited permissions from a textbox against indirect roles."""
        saved_permissions = text_box.get("1.0", "end-1c").split("##")[1:]

        if len(saved_permissions) != len(indirect_roles):
            return []
        else:
            for n in range(len(saved_permissions)):
                saved_permissions[n] = f"##{saved_permissions[n]}"
            return saved_permissions

    def save_edited_permissions(self, role, base_path, saved_permissions_iter):
        """Save the next edited permission string for a role to its file."""
        with open(self.pathfinder.get_permissions(role, base_path), "w") as file:
            file.write(next(saved_permissions_iter))
