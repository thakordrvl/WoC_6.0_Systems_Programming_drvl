import os
import sys
import shutil

def get_file_extension(file_name):
    file_extension = os.path.splitext(file_name)[1]
    return file_extension.upper()  # Convert to uppercase for consistency

def move_file_to_folder(file_path, destination_folder):
    # Move the file to the destination folder
    shutil.move(file_path, destination_folder)

def create_folder_if_not_exists(folder_path):
    # Create the folder and its parent directories if they don't exist
    os.makedirs(folder_path, exist_ok=True)

current_directory_from_user = input("Enter Your path: ")
# current_directory_from_CLA = sys.argv[1];

files_and_directories = os.listdir(current_directory_from_user)

for item in files_and_directories:
    item_path = os.path.join(current_directory_from_user, item)
    
    if os.path.isfile(item_path):
        file_extension = get_file_extension(item)
        dir_name = file_extension + " FILES"
        dir_path = os.path.join(current_directory_from_user, dir_name)
        
        if os.path.exists(dir_path):
            move_file_to_folder(item_path, dir_path)
            
        elif not os.path.exists(dir_path):
            create_folder_if_not_exists(dir_path)
            move_file_to_folder(item_path, dir_path)
