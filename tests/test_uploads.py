import os
from http import HTTPStatus

import pytest

from app import create_app
from app.services.file_manager import get_and_delete_last_created_txt_file

TEST_DATA_FOLDER = "tests\\data\\"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    yield client
    # Clean up after each test
    get_and_delete_last_created_txt_file(app.config["UPLOAD_FOLDER"])


def test_upload_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "allowed_text.txt")
    data = {"file": (open(file_path, "rb"), "allowed_text.txt")}

    # Make a POST request to the '/upload' endpoint
    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.CREATED
    assert b"File uploaded successfully" in response.data


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

    # Make a POST request to the '/upload' endpoint
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
