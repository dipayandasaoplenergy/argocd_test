import os

import os
import shutil

def cleaner_function(root,dir_name):
    pycache_path = os.path.join(root, dir_name)
    try:
        shutil.rmtree(pycache_path)
        print(f"Deleted: {pycache_path}")
    except Exception as e:
        print(f"Failed to delete {pycache_path}: {e}")

def delete_pycache_folders(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cleaner_function(root,dir_name)


def print_tree(root_dir, prefix="", ignore_dirs=None):
    """Recursively prints a tree view of the given directory, ignoring given dirs."""
    if ignore_dirs is None:
        ignore_dirs = ["venv", "__pycache__"]

    # Filter items, remove ignored directories
    items = [i for i in sorted(os.listdir(root_dir)) if i not in ignore_dirs]
    pointers = ["├── "] * (len(items) - 1) + ["└── "]

    for pointer, item in zip(pointers, items):
        path = os.path.join(root_dir, item)
        print(prefix + pointer + item)
        if os.path.isdir(path):
            extension = "│   " if pointer == "├── " else "    "
            print_tree(path, prefix + extension, ignore_dirs)


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Cleaning __pycache__ folders from: {current_dir}")
    delete_pycache_folders(current_dir)
    print("Cleanup complete!")
    folder = current_dir  # Change this to any path you want
    print(folder)
    print_tree(folder)
