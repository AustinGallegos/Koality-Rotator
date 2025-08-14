from .interfaces import (AssignmentManagerInterface, PermissionsManagerInterface,
                         CustomizationManagerInterface, ScheduleFinderInterface,
                         FilePathInterface, BusinessLogicInterface)


class ScheduleBusinessLogic(BusinessLogicInterface):
    def __init__(self, assignment_manager: AssignmentManagerInterface,
                 permissions_manager: PermissionsManagerInterface,
                 customization_manager: CustomizationManagerInterface,
                 schedule_finder: ScheduleFinderInterface,
                 pathfinder: FilePathInterface):
        self.assignment_manager = assignment_manager
        self.permissions_manager = permissions_manager
        self.customization_manager = customization_manager
        self.schedule_finder = schedule_finder
        self.pathfinder = pathfinder
        self.temp_path, self.base_path = pathfinder.get_paths()

    def assign_indirects(self, nums_dict, scheduled_associates):
        return self.assignment_manager.assign_indirects(nums_dict, scheduled_associates, self.base_path)

    def save_permissions(self, text):
        return self.permissions_manager.save_permissions(self.base_path, text)

    def check_permissions(self):
        return self.permissions_manager.check_permissions(self.base_path)

    def get_shifts(self):
        return self.customization_manager.get_shifts(self.base_path)

    def get_roles(self):
        return self.customization_manager.get_roles(self.base_path)

    def save(self, filename, text_list):
        return self.customization_manager.save(filename, text_list, self.base_path)

    def get_site(self):
        return self.customization_manager.get_site(self.base_path)

    def get_scheduled_associates(self, display_manager):
        return self.schedule_finder.get_scheduled_associates(display_manager)
