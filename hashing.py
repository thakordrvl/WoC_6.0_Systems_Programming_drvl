import os
import shutil
import hashlib
import json

def write_to_json(json_array, json_file_path):
    """
    Write a JSON array to a file.

    Args:
        json_array (list): The list containing JSON-compatible data.
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """

    # Open the specified JSON file in write mode
    with open(json_file_path, 'w') as json_file:
        # Dump the JSON array to the file with indentation for readability
        json.dump(json_array, json_file, indent=2)

def compute_md5(file_path):
    """
    Compute the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.
    """

    # Set initial and maximum chunk sizes for reading the file
    initial_chunk_size = 4096
    max_chunk_size = 65536

    # Initialize MD5 hash object
    hash_md5 = hashlib.md5()
    chunk_size = initial_chunk_size

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the file in chunks and update the MD5 hash
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_md5.update(chunk)
            # Dynamically adjust chunk size for efficiency
            if chunk_size < max_chunk_size:
                chunk_size *= 2

    # Return the hexadecimal representation of the MD5 hash
    return hash_md5.hexdigest()

def get_file_info(file_path):
    """
    Get file information including filename, file size, and MD5 hash.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: Dictionary containing file information.
    """

    # Get the file size using os.path.getsize
    file_size = os.path.getsize(file_path)
    # Compute the MD5 hash using the compute_md5 function
    md5_hash = compute_md5(file_path)

    # Return a dictionary containing file information
    return {"Filename": os.path.basename(file_path), "file size": file_size, "md5 hash": md5_hash}

def Generating_hash_file(input_directory):
    """
    Generate file information for all files in a directory and write to a JSON file.

    Args:
        input_directory (str): The path to the directory.

    Returns:
        None
    """

    # Get the list of files and directories in the specified directory
    files_and_directories = os.listdir(input_directory)
    files_in_json = []

    # Iterate through each item in the directory
    for item in files_and_directories:
        # Construct the full path to the item
        item_path = os.path.join(input_directory, item)

        # Check if the item is a file
        if os.path.isfile(item_path):
            # Append file information to the list
            files_in_json.append(get_file_info(item_path))

    # Create the path for the output JSON file
    json_file_path = os.path.join(input_directory, "file_info.json")

    # Call the write_to_json function to write the list to a JSON file
    write_to_json(files_in_json, json_file_path)
    print("JSON file successfully created/updated at " + input_directory)

def copy_directory(source_path, destination_path):
    """
    Copy a directory to a destination and generate file information in a JSON file.

    Args:
        source_path (str): The path to the source directory.
        destination_path (str): The path to the destination directory.

    Returns:
        None
    """

    # Get the base name of the source directory
    source_directory_name = os.path.basename(os.path.normpath(source_path))
    # Create the full path to the destination directory
    full_destination_path = os.path.join(destination_path, source_directory_name)

    # Check if the destination directory already exists
    if os.path.exists(full_destination_path):
        # Ask the user if they want to replace the existing directory
        ans = input("There exists a directory with the same name. Enter YES if you want to replace the existing directory ")
        
        # If the user agrees, remove the existing directory
        if ans != "YES":
            print("Exiting program. Please recompile if you want to generate hash files or copy directories. ")
            exit()
        shutil.rmtree(full_destination_path)

    # Copy the source directory to the destination
    shutil.copytree(source_path, full_destination_path)
    print("Directory successfully copied at " + destination_path)

    # Generate file information for the copied directory
    Generating_hash_file(full_destination_path)

# Input validation
current_directory_from_user = input("Please enter the path of the directory where you want to creat JSON file : ")
if os.path.exists(current_directory_from_user) == False:
    print("Invalid path. Kindly recompile.")
    exit()

# Generate file information for the specified directory
Generating_hash_file(current_directory_from_user)

# Get user input for the source and destination paths
source_path = input("Please enter the path of the directory you want to copy : ")
destination_path = input("Please enter the path of the directory where you want to place the copied directory : ")

# Check if the source and destination paths are valid and source path is directory
if (os.path.exists(source_path) == False or os.path.exists(destination_path) == False ):        
    print("Invalid source/destination path. Kindly recompile.")
    exit()
    
if(os.path.isdir(source_path)==False):
    print("Source path is not a directory")
    exit()

# Copy the directory and generate file information for the copied directory
copy_directory(source_path, destination_path)

print("hello world")
