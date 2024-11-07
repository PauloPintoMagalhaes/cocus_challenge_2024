import os
import random
import re

from services.file_manager import get_last_uploaded_text_file_path


def get_file_contents(file_path):
    file_data = []
    file_name = None
    if file_path and os.path.isfile(file_path):
        with open(file_path, "rb") as file_text:
            file_name = os.path.basename(file_path)
            for index, text_line in enumerate(file_text):
                if re.search(rb"\S", text_line):
                    file_data.append((index, text_line.strip()))
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
