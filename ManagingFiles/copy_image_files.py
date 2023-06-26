import os
import shutil


def copy_images(source_dir, destination_dir):
    # Get a list of all files in the source directory
    file_list = os.listdir(source_dir)

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Copy image files from source to destination directory
    for file in file_list:
        # Check if the file has an image extension
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.copy2(source_path, destination_path)
            print(f"Copied {file} to {destination_dir}")
