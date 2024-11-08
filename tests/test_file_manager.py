import os

from app.services.file_manager import (
    get_all_text_file_path_list,
    get_and_delete_last_created_txt_file,
    get_random_text_file_path,
)
from app.services.text_manager import get_last_uploaded_text_file_path
from tests.test_routes import TEST_DATA_FOLDER


def test_get_text_path_list():
    file_path_list = get_all_text_file_path_list(TEST_DATA_FOLDER)

    assert file_path_list == [
        "tests\\data\\allowed_text.txt",
        "tests\\data\\big_allowed_text.txt",
        "tests\\data\\empty_text.txt",
        "tests\\data\\max_size_text.txt",
    ]


def test_get_random_text_file_path():
    file_path_list = get_all_text_file_path_list(TEST_DATA_FOLDER)
    random_path_file = get_random_text_file_path(TEST_DATA_FOLDER)

    # Testing randomness is not possible, hence test that the
    # result exists in the list of text files
    assert random_path_file in file_path_list


def test_get_last_uploaded_text_file_path():
    file_path = get_last_uploaded_text_file_path(TEST_DATA_FOLDER)
    assert file_path == "tests\\data\\big_allowed_text.txt"


def test_get_and_delete_last_created_txt_file():
    # Create a sample .txt file in the test directory
    test_file_path = os.path.join(TEST_DATA_FOLDER, "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("This is a test file.")

    assert os.path.exists(test_file_path) is True
    get_and_delete_last_created_txt_file(TEST_DATA_FOLDER)
    assert os.path.exists(test_file_path) is False
