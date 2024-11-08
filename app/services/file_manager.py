import os
import random
from glob import glob


def get_text_file_path_list(folder):
    return glob(os.path.join(folder, "*.txt"))


def get_random_text_file_path(folder):
    return random.choice(get_text_file_path_list(folder))


def get_last_uploaded_text_file_path(folder):
    if files := get_text_file_path_list(folder):
        return max(files, key=os.path.getctime)


def get_and_delete_last_created_txt_file(folder):
    if last_file := get_last_uploaded_text_file_path(folder):
        os.remove(last_file)
