import pytest
from unittest.mock import Mock
from managers import DisplayManager
from utils import ScheduleBusinessLogic
from utils.interfaces import (AssignmentManagerInterface, PermissionsManagerInterface,
                              CustomizationManagerInterface, ScheduleFinderInterface, FilePathInterface)


@pytest.fixture()
def mock_business_logic():
    assignment_manager = Mock(spec=AssignmentManagerInterface)
    permissions_manager = Mock(spec=PermissionsManagerInterface)
    customization_manager = Mock(spec=CustomizationManagerInterface)
    schedule_finder = Mock(spec=ScheduleFinderInterface)
    pathfinder = Mock(spec=FilePathInterface)
    pathfinder.get_paths.return_value = ("/tmp", "/base")

    return ScheduleBusinessLogic(assignment_manager,
                                 permissions_manager,
                                 customization_manager,
                                 schedule_finder,
                                 pathfinder)


@pytest.fixture()
def mock_display_manager():
    display_manager = Mock(spec=DisplayManager)
    display_manager.driver = Mock()
    display_manager.shift = Mock()
    display_manager.date = Mock()

    return display_manager


@pytest.mark.parametrize(
    "nums_dict, scheduled_associates",
    [
        ({"End of Line": 1}, ["dayvinc"]),
        ({"End of Line": 1}, ["galleaus"]),
        ({"End of Line": 1, "Problem Solve": 1}, ["dayvinc", "galleaus"])
    ]
)
def test_assign_indirects(mock_business_logic,
                          nums_dict,
                          scheduled_associates):
    business_logic = mock_business_logic
    business_logic.assign_indirects(nums_dict, scheduled_associates)

    business_logic.assignment_manager.assign_indirects.assert_called_once_with(nums_dict,
                                                                               scheduled_associates,
                                                                               business_logic.base_path)


@pytest.mark.parametrize(
    "text",
    ["# Problem Solve\n# MOR Shift\ngalleaus",
     "# End of Line\n# DAY Shift\ngalleaus",
     "# Audit\n#NIT Shift\ngalleaus"
     ]
)
def test_save_permissions(mock_business_logic, text):
    business_logic = mock_business_logic
    business_logic.save_permissions(text)
    business_logic.permissions_manager.save_permissions.assert_called_once_with(business_logic.base_path,
                                                                                text)


def test_check_permissions(mock_business_logic):
    business_logic = mock_business_logic
    business_logic.check_permissions()
    business_logic.permissions_manager.check_permissions.assert_called_once_with(business_logic.base_path)


def test_get_shifts(mock_business_logic):
    business_logic = mock_business_logic
    business_logic.get_shifts()
    business_logic.customization_manager.get_shifts.assert_called_once_with(business_logic.base_path)


def test_get_roles(mock_business_logic):
    business_logic = mock_business_logic
    business_logic.get_roles()
    business_logic.customization_manager.get_roles.assert_called_once_with(business_logic.base_path)


@pytest.mark.parametrize(
    "filename, text_list",
    [
        ("site", ["SMF9"]),
        ("saved_shifts", ["04-00-00", "09-30-00"]),
        ("saved_roles", ["End of Line", "Problem Solve"])
    ]
)
def test_save(mock_business_logic, filename, text_list):
    business_logic = mock_business_logic
    business_logic.save(filename, text_list)
    business_logic.customization_manager.save.assert_called_once_with(filename, text_list, business_logic.base_path)


def test_get_site(mock_business_logic):
    business_logic = mock_business_logic
    business_logic.get_site()
    business_logic.customization_manager.get_site.assert_called_once_with(business_logic.base_path)


def test_get_scheduled_associates(mock_business_logic, mock_display_manager):
    business_logic = mock_business_logic
    display_manager = mock_display_manager

    business_logic.get_scheduled_associates(display_manager)
    business_logic.schedule_finder.get_scheduled_associates.assert_called_once_with(display_manager)

