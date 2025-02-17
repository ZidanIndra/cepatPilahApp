import os

def validate_image_file(file_path):
    """Validates if a file is an image."""
    valid_extensions = ('.png', '.jpg', '.jpeg')
    return file_path.lower().endswith(valid_extensions)

def create_folder_if_not_exists(folder_path):
    """Creates a folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)