import os
import shutil
import hashlib

# print(hashlib.algorithms_guaranteed)
current_directory_from_user = input("Enter your path: ")

if(os.path.exists(current_directory_from_user)==False):
    print("Invalid path kindly recompile")
    exit()

files_and_directories = os.listdir(current_directory_from_user)
files_in_json = []

def compute_md5(file_path):
    initial_chunk_size = 4096
    max_chunk_size = 65536
    hash_md5 = hashlib.md5()
    chunk_size = initial_chunk_size

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_md5.update(chunk)
            # Dynamically adjust chunk size
            if chunk_size < max_chunk_size:
                chunk_size *= 2

    return hash_md5.hexdigest()


def get_file_info(file_path):
    file_size = os.path.getsize(file_path)
    md5_hash = compute_md5(file_path)
    return {"Filename": os.path.basename(file_path), "file size": file_size, "md5 hash": md5_hash}

def Generating_hash_files(input_directory):

    for item in files_and_directories:
        item_path = os.path.join(input_directory, item)
        
        if os.path.isfile(item_path):
            files_in_json.append(get_file_info(item_path))
                
Generating_hash_files(current_directory_from_user)
print(files_in_json)
