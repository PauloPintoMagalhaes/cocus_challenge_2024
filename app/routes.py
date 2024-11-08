import os
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, render_template, request

from app.services.text_manager import (
    get_random_line_from_last_file,
    get_reversed_random_line_from_all_files,
)
from config.constants import UPLOAD_FOLDER
from config.validations import (
    validate_file_has_text,
    validate_file_is_selected,
    validate_file_size,
    validate_file_type,
)

routes = Blueprint("routes", __name__)


# Because I'm lazy and I don't want to memorize commands
# Let's make an interface for this.
@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    error = validate_file_is_selected(file)
    if error:
        return error

    error = validate_file_type(file)
    if error:
        return error

    file_read = file.read()
    error = validate_file_has_text(file_read)
    if error:
        return error

    error = validate_file_size(file_read)
    if error:
        return error

    # This is needed because file.read() puts the pointer of the
    # file and the end, causing the save function to save an empty file
    file.seek(0)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return (
        jsonify(
            {"message": "File uploaded successfully", "file_path": file_path}
        ),
        HTTPStatus.CREATED,
    )


@routes.route("/random_line", methods=["GET"])
def random_line():
    line_data = get_random_line_from_last_file(UPLOAD_FOLDER)
    accepted_headers = request.headers.get("Accept", "")

    if line_data:
        if "application/json" in accepted_headers:
            response_data = {
                "line": line_data["line"],
                "line_number": line_data["line_num"],
                "file_name": line_data["file_name"],
                "most_frequent_letter": line_data["most_frequent_letter"],
            }
            return jsonify(response_data), HTTPStatus.OK

        elif "application/xml" in accepted_headers:
            response_xml = (
                f"<line>{line_data['line']}</line>"
                f"<line_number>{line_data['line_num']}</line_number>"
                f"<file_name>{line_data['file_name']}</file_name>"
                f"<most_frequent_letter>{line_data['most_frequent_letter']}"
                "</most_frequent_letter>"
            )
            return (
                Response(response_xml, mimetype="application/xml"),
                HTTPStatus.OK,
            )

        else:
            # Defaults to text/plain
            return (
                Response(line_data["line"], mimetype="text/plain"),
                HTTPStatus.OK,
            )

    # Returns OK, because it's not an error. There's just no info to give.
    return (
        jsonify({"message": "No files with valid text exist."}),
        HTTPStatus.OK,
    )


@routes.route("/reversed_random_line", methods=["GET"])
def reversed_random_line():
    line_data = get_reversed_random_line_from_all_files(UPLOAD_FOLDER)
    return (
        jsonify({"line": line_data}),
        HTTPStatus.OK,
    )


# TODO This needs error logging
