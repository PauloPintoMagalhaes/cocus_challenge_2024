import os
import re

from flask import Flask, jsonify, render_template, request

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}
KILOBYTE_SIZE = 1024
MAX_FILE_SIZE_ALLOWED = KILOBYTE_SIZE * 5  # 5Kb Max file size


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def is_allowed_file_type(filename):
    # Though the upload form checks for the correct file type
    # I'd rather have the redundancy
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Because I'm lazy and I don't want to memorize commands
# Let's make an interface for this.
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if the file part is present in the request
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    # While the html form should prevent these, there's the possibility
    # this might be called by command line. Best check for redundancy.
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not is_allowed_file_type(file.filename):
        return (
            jsonify({"error": "File type not allowed, only .txt files"}),
            400,
        )

    # Ensure the file size isn't over the limit we allow and that
    # it isn't a file without proper text
    file_read = file.read()
    if not re.search(rb"\S", file_read):
        return jsonify({"error": "File has no text"}), 400
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
            400,
        )
    # This is needed because file.read() puts the pointer of the
    # file and the end, causing the save function to save an empty file
    file.seek(0)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return (
        jsonify(
            {"message": "File uploaded successfully", "file_path": file_path}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
