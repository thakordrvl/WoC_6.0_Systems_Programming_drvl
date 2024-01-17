import os
import shutil
import hashlib

# current_directory_from_user = input("Enter your path: ")

# if(os.path.exists(current_directory_from_user)==False):
#     print("Invalid path kindly recompile")
#     exit()


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

    files_and_directories = os.listdir(input_directory)
    files_in_json = []
    
    for item in files_and_directories:
        item_path = os.path.join(input_directory, item)
        # print(item)
        
        if os.path.isfile(item_path):
            files_in_json.append(get_file_info(item_path))
            
    return files_in_json        

def copy_directory(source_path, destination_path):
    
    source_directory_name = os.path.basename(os.path.normpath(source_path))
    full_destination_path = os.path.join(destination_path, source_directory_name)
    
    print("reached here")
    
    if os.path.exists(full_destination_path):
                
        ans = input("There exist a directory with the same name please enter YES if you want to replace the existing directory ")
        
        if ans!="YES" : 
            print("exiting program please recomplile")
            exit()
            
        shutil.rmtree(full_destination_path)
        
    shutil.copytree(source_path,full_destination_path)
    
    return Generating_hash_files(full_destination_path)
        
        
# files_in_json = Generating_hash_files(current_directory_from_user)
source_path = input("please enter the path of the directory you want to copy : ")
destination_path = input("please enter the path of the directory where you want to place the copied directory : ")
files_in_json_after_copying = copy_directory(source_path,destination_path)
print(files_in_json_after_copying)
