import random
from utils.interfaces import AssignmentManagerInterface, FilePathInterface


class AssignmentManager(AssignmentManagerInterface):
    def __init__(self, pathfinder: FilePathInterface):
        self.pathfinder = pathfinder

    def assign_indirects(self, nums_dict, scheduled_associates, base_path):
        """Assigns indirect roles based on user's inputs on main menu."""
        nums_list = self.get_nonzero_keys(nums_dict)
        random.shuffle(nums_list)

        result_string = ""
        not_enough_string = ""
        chosen_associates = set()

        for key in nums_list:
            trained_associates = self.get_trained_associates(key, base_path)
            result, not_enough = self.assign_roles_to_associates(key, nums_dict[key],
                                                                 trained_associates, scheduled_associates,
                                                                 chosen_associates)

            result_string += result
            not_enough_string += not_enough

        return result_string, not_enough_string

    def get_nonzero_keys(self, nums_dict):
        """Returns the keys from nums_dict that have non-zero values."""
        return [key for key, val in nums_dict.items() if val != 0]

    def get_trained_associates(self, key, base_path):
        """Retrieve and shuffle the list of trained associates from a file."""
        with open(self.pathfinder.get_custom_text(base_path, key)) as file:
            trained_associates = file.read().split("\n")
            trained_associates = [associate for associate in trained_associates if associate]  # Remove empty lines
            random.shuffle(trained_associates)
            return trained_associates

    def assign_roles_to_associates(self, key, nums_roles, trained_associates, scheduled_associates, chosen_associates):
        """Assign available trained associates to specific roles."""
        result = ""
        not_enough = ""
        empty = False
        for _ in range(nums_roles):
            while True:
                try:
                    choice = trained_associates.pop()
                except IndexError:
                    not_enough += f"Not enough eligible AAs to fill {key}.\n"
                    empty = True
                    break

                else:
                    if choice not in scheduled_associates:
                        continue

                    if choice not in chosen_associates:
                        chosen_associates.add(choice)
                        result += f"{key}: {choice}\n"
                        break

            if empty:
                break

        return result, not_enough
