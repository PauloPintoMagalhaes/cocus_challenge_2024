import re
from http import HTTPStatus

from flask import jsonify

from config.constants import (
    ALLOWED_EXTENSIONS,
    KILOBYTE_SIZE,
    MAX_FILE_SIZE_ALLOWED,
)


def _is_allowed_file_type(filename):
    """
    Check if a given file has an allowed extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed extension as per
            `ALLOWED_EXTENSIONS`, False otherwise.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_file_is_selected(file):
    """
    Validate if a file has a valid filename.
    This function ensures that the file has a non-empty filename,
    adding redundancy against invalid file uploads.

    Args:
        file (FileStorage): The file object uploaded by the user.

    Returns:
        Response: A JSON response with an error message and HTTP 400 status
            if the filename is valid, otherwise None if the file passes
            validation.
    """
    if file.filename == "":
        return jsonify({"error": "No selected file"}), HTTPStatus.BAD_REQUEST


def validate_file_type(file):
    """
    Validate if a file has a valid and extension.
    This function ensures that the file has a valid
    extension, adding redundancy against invalid file uploads.

    Args:
        file (FileStorage): The file object uploaded by the user.

    Returns:
        Response: A JSON response with an error message and HTTP 400 status
            if the file is invalid, otherwise None if the file passes
            validation.
    """
    if not _is_allowed_file_type(file.filename):
        return (
            jsonify({"error": "File type not allowed, only .txt files"}),
            HTTPStatus.BAD_REQUEST,
        )


def validate_file_has_text(file_read):
    """
    Check if a file contains non-whitespace text.

    Args:
        file_read (bytes): The file content read as bytes.

    Returns:
        Response: A JSON response with an error message and HTTP 400 status
            if the file has no text content, otherwise None if text is
            present.
    """
    if not re.search(rb"\S", file_read):
        return jsonify({"error": "File has no text"}), HTTPStatus.BAD_REQUEST


def validate_file_size(file_read):
    """
    Check if a file's size is within the allowed limit.

    Args:
        file_read (bytes): The file content read as bytes.

    Returns:
        Response: A JSON response with an error message and HTTP 400 status
            if the file size exceeds `MAX_FILE_SIZE_ALLOWED`, otherwise None
            if the file size is within the limit.
    """
    if len(file_read) > MAX_FILE_SIZE_ALLOWED:
        return (
            jsonify(
                {
                    "error": (
                        "File exceeds the maximum size of "
                        f"{MAX_FILE_SIZE_ALLOWED / KILOBYTE_SIZE} KB"
                    )
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )
