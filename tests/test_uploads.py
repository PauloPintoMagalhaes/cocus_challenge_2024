import os
import sys

import pytest

# TODO find a way to get rid of this.
# It displeases me profoundly.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from app import UPLOAD_FOLDER, app  # noqa

TEST_DATA_FOLDER = "tests/data/"


@pytest.fixture
def client():
    # Set up a test client for the Flask app
    app.config["TESTING"] = True
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    client = app.test_client()
    yield client
    # Clean up after each test
    # TODO: For now this cleans every file even those manually uploaded.
    # we want to change that later
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def test_upload_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "allowed_text.txt")
    data = {"file": (open(file_path, "rb"), "allowed_text.txt")}

    # Make a POST request to the '/upload' endpoint
    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 201
    assert b"File uploaded successfully" in response.data


def test_no_file(client):
    # Simulate a POST request without a file
    response = client.post("/upload", data={})
    assert response.status_code == 400
    assert b"No file part" in response.data


def test_empty_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "empty_text.txt")
    data = {"file": (open(file_path, "rb"), "empty_text.txt")}
    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert b"File has no text" in response.data


def test_oversized_file(client):
    file_path = os.path.join(TEST_DATA_FOLDER, "max_size_text.txt")
    data = {"file": (open(file_path, "rb"), "max_size_text.txt")}
    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert b"File exceeds the maximum size of 5.0 KB" in response.data
