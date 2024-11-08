import os
import random

from app.services.file_manager import (
    get_all_text_file_path_list,
    get_last_uploaded_text_file_path,
)


def get_file_contents(file_path):
    file_data = []
    file_name = None

    if file_path and os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file_text:
            for index, text_line in enumerate(file_text, start=1):
                stripped_line = text_line.strip()
                if stripped_line:
                    file_data.append((index, stripped_line))
    return file_data, file_name


def _get_most_frequent_letter(text):
    letters = [c.lower() for c in text if c.isalpha()]
    return max(set(letters), key=letters.count) if letters else None


def get_random_line_from_last_file(folder):
    file_text, file_name = get_file_contents(
        get_last_uploaded_text_file_path(folder)
    )
    if file_text and file_name:
        random_text_line = random.choice(file_text)
        line = random_text_line[1].decode("utf-8")
        return {
            "line": line,
            "line_num": random_text_line[0],
            "file_name": file_name,
            "most_frequent_letter": _get_most_frequent_letter(line),
        }


def _get_contents_from_all_files(folder):
    file_paths = get_all_text_file_path_list(folder)
    return [
        text_line
        for file_path in file_paths
        for text_line in get_file_contents(file_path)[0]
    ]


def get_reversed_random_line_from_all_files(folder):
    all_text_data = _get_contents_from_all_files(folder)
    if not all_text_data:
        return None

    _, line_content = random.choice(all_text_data)
    return line_content.decode("utf-8")[::-1]
