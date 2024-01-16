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
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
            
    return file_hash.hexdigest()

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
