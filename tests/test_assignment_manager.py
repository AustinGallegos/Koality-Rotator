import os
import pytest
from unittest.mock import Mock, mock_open, patch
from managers import AssignmentManager
from utils import FilePath


@pytest.fixture()
def assignment_manager():
    pathfinder = Mock(spec=FilePath)
    pathfinder.get_custom_text.return_value = "fakefile.txt"
    return AssignmentManager(pathfinder)


@pytest.fixture()
def base_path():
    return os.path.dirname(__file__)


@pytest.mark.parametrize("nums_dict, scheduled_associates, expected_result, expected_enough",
                         [
                             ({"End of Line": 1}, ["dayvinc"], "End of Line: dayvinc\n", ""),
                             ({"End of Line": 1}, ["galleaus"], "", "Not enough eligible AAs to fill End of Line.\n"),
                             ({"End of Line": 2}, ["dayvinc"], "End of Line: dayvinc\n",
                              "Not enough eligible AAs to fill End of Line.\n")
                         ])
def test_assign_indirects(assignment_manager,
                          base_path,
                          nums_dict,
                          scheduled_associates,
                          expected_result,
                          expected_enough):
    fake_file_content = "# MOR Shift\ndayvinc\n"

    with patch("builtins.open", mock_open(read_data=fake_file_content)):
        result_string, not_enough_string = assignment_manager.assign_indirects(nums_dict, scheduled_associates, base_path)
        assert result_string == expected_result
        assert not_enough_string == expected_enough


@pytest.mark.parametrize("nums_dict, expected_result",
                         [
                             ({"End of Line": 1, "Problem Solve": 1, "Audit": 1},
                              ["End of Line", "Problem Solve", "Audit"]),
                             ({"End of Line": 0, "Problem Solve": 1, "Audit": 2},
                              ["Problem Solve", "Audit"]),
                             ({"End of Line": 0, "Problem Solve": 0, "Audit": 0},
                              [])
                         ])
def test_nonzero_keys(assignment_manager, nums_dict, expected_result):
    result = assignment_manager.get_nonzero_keys(nums_dict)
    assert result == expected_result
