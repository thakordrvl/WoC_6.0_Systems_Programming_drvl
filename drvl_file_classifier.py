import os
import shutil

def get_file_extension(file_name):
    # Get the file extension and convert it to uppercase for consistency
    return os.path.splitext(file_name)[1][1:].upper()

def move_file_to_folder(file_path, destination_folder):
    # Move the file to the destination folder
    shutil.move(file_path, destination_folder)

def create_folder_if_not_exists(folder_path):
    # Create the folder and its parent directories if they don't exist
    os.makedirs(folder_path, exist_ok=True)

def organize_files_by_extension(input_directory):
    # Get the list of files and directories in the specified directory
    files_and_directories = os.listdir(input_directory)

    # Iterate through each item in the directory
    for item in files_and_directories:
        item_path = os.path.join(input_directory, item)

        # Check if the item is a file
        if os.path.isfile(item_path):
            # Get the file extension excluding the dot
            file_extension = get_file_extension(item)
            
            # Create a directory name for the specific extension
            dir_name = "ALL " + file_extension + " FILES"
            
            # Construct the full path for the destination directory
            dir_path = os.path.join(input_directory, dir_name)

            # Check if the destination directory already exists
            if os.path.exists(dir_path):
                move_file_to_folder(item_path, dir_path)
            else:
                # Create the destination directory if it doesn't exist
                create_folder_if_not_exists(dir_path)
                move_file_to_folder(item_path, dir_path)

# Get user input for the directory path
current_directory_from_user = input("Enter your path: ")
# Call the function to organize files in the specified directory

if(os.path.exists(current_directory_from_user)==False):
    print("Invalid path kindly recompile")
    exit()
    
organize_files_by_extension(current_directory_from_user)

