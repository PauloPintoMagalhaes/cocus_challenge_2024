import os

import pytest
from test_uploads import TEST_DATA_FOLDER

from app.services.text_manager import get_file_contents


@pytest.mark.parametrize(
    "input_file_name, expected_file_data, expected_file_name",
    [
        # Happy path
        (
            "allowed_text.txt",
            [
                (0, b"This is the first line"),
                (1, b"This is the second line"),
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
