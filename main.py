import utils
import managers


def main():
    pathfinder = utils.FilePath()
    temp_path, base_path = pathfinder.get_paths()
    pathfinder.app_init(temp_path, base_path)

    smile_logo = pathfinder.get_image_path(temp_path, base_path, "image1.png")
    koala_logo = pathfinder.get_image_path(temp_path, base_path, "image2.ico")
    paths_dict = {"temp_path": temp_path,
                  "base_path": base_path,
                  "smile_logo": smile_logo,
                  "koala_logo": koala_logo}

    assignment_manager = managers.AssignmentManager(pathfinder)
    permissions_manager = managers.PermissionsManager(pathfinder)
    customization_manager = managers.CustomizationManager(pathfinder)
    schedule_finder = utils.ScheduleFinder()

    business_logic = utils.ScheduleBusinessLogic(assignment_manager,
                                                 permissions_manager,
                                                 customization_manager,
                                                 schedule_finder,
                                                 pathfinder)

    managers.DisplayManager(paths_dict, business_logic)


if __name__ == "__main__":
    main()
