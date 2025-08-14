from abc import ABC, abstractmethod


class AssignmentManagerInterface(ABC):
    @abstractmethod
    def assign_indirects(self, nums_dict, scheduled_associates, base_path):
        pass


class PermissionsManagerInterface(ABC):
    @abstractmethod
    def save_permissions(self, base_path, text):
        pass

    @abstractmethod
    def check_permissions(self, base_path):
        pass


class CustomizationManagerInterface(ABC):
    @abstractmethod
    def get_shifts(self, base_path):
        pass

    @abstractmethod
    def get_roles(self, base_path):
        pass

    @abstractmethod
    def save(self, filename, text_list, base_path):
        pass

    @abstractmethod
    def get_site(self, base_path):
        pass


class ScheduleFinderInterface(ABC):
    @abstractmethod
    def get_scheduled_associates(self, display_manager):
        pass


class FilePathInterface(ABC):
    @abstractmethod
    def get_paths(self):
        pass

    @abstractmethod
    def get_custom_text(self, base_path, param):
        pass

    @abstractmethod
    def get_permissions(self, role, base_path):
        pass


class BusinessLogicInterface(ABC):
    @abstractmethod
    def __init__(self, assignment_manager,
                 permissions_manager,
                 customization_manager,
                 schedule_finder,
                 pathfinder):
        pass
