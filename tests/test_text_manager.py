import os
from unittest.mock import patch

import pytest

from app.services.text_manager import (
    _get_contents_from_all_files,
    get_file_contents,
    get_reversed_random_line_from_all_files,
)
from tests.test_routes import TEST_DATA_FOLDER


@pytest.mark.parametrize(
    "input_file_name, expected_file_data, expected_file_name",
    [
        # Happy path
        (
            "allowed_text.txt",
            [
                (1, b"This is the first line"),
                (2, b"This is the second line"),
            ],
            "allowed_text.txt",
        ),
        # Not so happy path
        ("empty_text.txt", [], "empty_text.txt"),
        ("fake_file.txt", [], None),
    ],
)
def test_get_file_contents(
    input_file_name, expected_file_data, expected_file_name
):
    test_file_path = os.path.join(TEST_DATA_FOLDER, input_file_name)

    file_text, output_file_name = get_file_contents(test_file_path)
    assert output_file_name == expected_file_name
    assert file_text == expected_file_data


def test__get_contents_from_all_files():
    MOCK_FILE_PATHS = ["mock_folder/file1.txt", "mock_folder/file2.txt"]
    MOCK_FILE_CONTENTS_1 = [
        (1, b"First file, first line"),
        (2, b"First file, second line"),
    ]
    MOCK_FILE_CONTENTS_2 = [(1, b"Second file, only line")]
    # Mock the `get_all_text_file_path_list` and `get_file_contents` functions
    with patch(
        "app.services.text_manager.get_all_text_file_path_list",
        return_value=MOCK_FILE_PATHS,
    ) as mock_get_paths, patch(
        "app.services.text_manager.get_file_contents",
        side_effect=[
            (MOCK_FILE_CONTENTS_1, "file1.txt"),
            (MOCK_FILE_CONTENTS_2, "file2.txt"),
        ],
    ) as mock_get_contents:

        # Call the function to test
        result = _get_contents_from_all_files(TEST_DATA_FOLDER)

        # Define the expected result based on mock data
        expected_result = [
            (1, b"First file, first line"),
            (2, b"First file, second line"),
            (1, b"Second file, only line"),
        ]

        # Assertions
        assert result == expected_result
        mock_get_paths.assert_called_once_with(TEST_DATA_FOLDER)
        assert mock_get_contents.call_count == 2
        mock_get_contents.assert_any_call(MOCK_FILE_PATHS[0])
        mock_get_contents.assert_any_call(MOCK_FILE_PATHS[1])


def test_get_reversed_random_line_from_all_files():
    MOCK_ALL_TEXT_DATA = [
        (1, b"First line of first file"),
        (2, b"Second line of first file"),
        (3, b"First line of second file"),
    ]
    with patch(
        "app.services.text_manager._get_contents_from_all_files",
        return_value=MOCK_ALL_TEXT_DATA,
    ) as mock_get_contents, patch(
        "random.choice", return_value=(1, b"Example line")
    ) as mock_random_choice:

        result = get_reversed_random_line_from_all_files(TEST_DATA_FOLDER)

        expected_result = "enil elpmaxE"

        assert result == expected_result
        mock_get_contents.assert_called_once_with(TEST_DATA_FOLDER)
        mock_random_choice.assert_called_once()
