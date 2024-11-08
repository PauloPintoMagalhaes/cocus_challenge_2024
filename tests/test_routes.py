import os
from http import HTTPStatus
from unittest.mock import patch

import pytest

from app import create_app
from app.services.file_manager import get_and_delete_last_created_txt_file
from config.constants import UPLOAD_FOLDER

TEST_DATA_FOLDER = "tests\\data\\"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


def test_upload_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "allowed_text.txt")
    data = {"file": (open(file_path, "rb"), "allowed_text.txt")}

    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.CREATED
    assert b"File uploaded successfully" in response.data
    # Delete the added file from uploads
    get_and_delete_last_created_txt_file(UPLOAD_FOLDER)


def test_no_file(client):
    # Simulate a POST request without a file
    response = client.post("/upload", data={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert b"No file part" in response.data


def test_invalid_extension(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "allowed_text.txt")
    # NOTE: the file is being opened correctly, but it's in the
    # wrong naming format
    data = {"file": (open(file_path, "rb"), "allowed_text.pdf")}

    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert b"File type not allowed, only .txt files" in response.data


def test_empty_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "empty_text.txt")
    data = {"file": (open(file_path, "rb"), "empty_text.txt")}

    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert b"File has no text" in response.data


def test_oversized_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "max_size_text.txt")
    data = {"file": (open(file_path, "rb"), "max_size_text.txt")}

    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert b"File exceeds the maximum size of 5.0 KB" in response.data


@pytest.mark.parametrize(
    "accept_header, expected_line_data",
    [
        (
            "application/json",
            {
                "file_name": "test_text.txt",
                "line": "bilberry banana elderberry pear raspberry",
                "line_number": 24,
                "most_frequent_letter": "r",
            },
        ),
        (
            "application/xml",
            (
                "<line>bilberry banana elderberry pear raspberry</line>"
                "<line_number>24</line_number>"
                "<file_name>test_text.txt</file_name>"
                "<most_frequent_letter>r</most_frequent_letter>"
            ),
        ),
        (
            "text/plain",
            "bilberry banana elderberry pear raspberry",
        ),
    ],
)
def test_random_line(client, accept_header, expected_line_data):
    LINE_DATA = {
        "file_name": "test_text.txt",
        "line": "bilberry banana elderberry pear raspberry",
        "line_num": 24,
        "most_frequent_letter": "r",
    }
    with patch(
        "app.routes.get_random_line_from_last_file", return_value=LINE_DATA
    ) as mock_get_random_line_from_last_file:
        response = client.get(
            "/random_line", headers={"Accept": accept_header}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.mimetype == accept_header
        mock_get_random_line_from_last_file.assert_called_once()

        if accept_header == "application/json":
            assert response.get_json() == expected_line_data
        elif accept_header == "application/xml":
            assert response.data.decode("utf-8") == expected_line_data
        elif accept_header == "text/plain":
            assert response.data.decode("utf-8") == expected_line_data


def test_reversed_random_line(client):
    """
    This test is rather silly, give that we're patching a value into
    the only function called within the endpoint. We do it anyway, just
    To guarantee that the endpoint is called and returns a response
    """
    EXPECTED_RESPONSE = "!edoc doog yllaer si sihT"
    with patch(
        "app.routes.get_reversed_random_line_from_all_files",
        return_value=EXPECTED_RESPONSE,
    ):
        response = client.get("/reversed_random_line")

        # Check that the status is OK
        assert response.status_code == HTTPStatus.OK

        # Ensure the JSON response contains the mocked reversed line
        response_data = response.get_json()
        assert response_data == {"line": EXPECTED_RESPONSE}
