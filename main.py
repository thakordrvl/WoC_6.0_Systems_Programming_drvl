import os
import hashlib
import shutil
import json
import sys
import datetime
import platform

def write_to_json(json_array, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(json_array, json_file, indent=2)

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
            if chunk_size < max_chunk_size:
                chunk_size *= 2
    return hash_md5.hexdigest()

def get_file_info(file_path):
    file_size = os.path.getsize(file_path)
    md5_hash = compute_md5(file_path)
    return {"Filename": os.path.basename(file_path), "file size": file_size, "md5 hash": md5_hash}

def Generating_hash_file(input_directory):
    files_and_directories = os.listdir(input_directory)
    files_in_json = []
    for item in files_and_directories:
        item_path = os.path.join(input_directory, item)
        if os.path.isfile(item_path):
            files_in_json.append(get_file_info(item_path))

    json_file_path = os.path.join(input_directory, "file_info.json")
    write_to_json(files_in_json, json_file_path)
    print("JSON file successfully created/updated at " + input_directory)
    
def add_file(file_name):
    print()
        
def get_tracked_hashes(dir_path): 
    json_path = os.path.join(dir_path,".drvl/branches/main/index.json")
    
    try:
        with open(json_path, "r") as index_file:
            index_data = json.load(index_file)
            tracked_hashes = [file_info["md5 hash"] for file_info in index_data.values()]
            return tracked_hashes
    except FileNotFoundError:
        return []

def get_untracked_files(dir_path):
    tracked_hashes = get_tracked_hashes(dir_path)
    all_files = [file for file in os.listdir(dir_path) if os.path.isfile(file)]
    untracked_files = []

    for file in all_files:
        file_hash = compute_md5(file)
        if file_hash not in tracked_hashes:
            untracked_files.append(file)

    return untracked_files

def print_status(dir_path):
    untracked_files = get_untracked_files(dir_path)

    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            print(f"- {file}")
    else:
        print("No untracked files.")

def print_usage_help():
    print("drvl - A Version Control System.")
    print("drvl init - Initialize a new drvl repository")
    print("drvl add <file> - Add a file to the index")
    print("drvl commit -m <message> - Commit changes with a message")
    print("drvl rmadd <file> - Remove a file from the index")
    print("drvl rmcommit - Remove last commit")
    print("drvl log - Display commit log")
    print("drvl checkout <commit> - Checkout a specific commit")
    print("drvl help - To see this usage help")
    print("drvl status - To see status")
    print("drvl user show - To see present user")
    print("drvl user set <username> - To change user")
    print("drvl push <path> - To push your file to another folder")
    print("Created by - Dhruvil")

def drvl_makedirs(dir_path, user_name):
    drvl_path = os.path.join(dir_path, ".drvl")  # Add a space before ".drvl"
    os.makedirs(drvl_path)
    
    # Check if the platform is Windows
    if platform.system() == 'Windows':
        # Use the attrib command to mark the directory as hidden
        attrib_cmd = f'attrib +h "{drvl_path}"'
        os.system(attrib_cmd)
            
    drvl_subpath_branches = os.path.join(drvl_path, "branches")
    drvl_subpath_objects = os.path.join(drvl_path, "objects")
    os.makedirs(drvl_subpath_branches)
    os.makedirs(drvl_subpath_objects)
    drvl_subpath_main_branches = os.path.join(drvl_subpath_branches, "main")
    os.makedirs(drvl_subpath_main_branches)
    drvl_userstxt_path = os.path.join(drvl_subpath_main_branches, "users")
    current_date_time = datetime.datetime.now()

    with open(drvl_userstxt_path, "w") as file:
        file.write(f"Date: {current_date_time.strftime('%Y-%m-%d')}\n")
        file.write(f"Timestamp: {current_date_time.strftime('%H:%M:%S')}\n")
        file.write("User: " + user_name)
        file.write("\n\n")
        
def isexist(file_name, path):
    files_directories = os.listdir(path)
    
    for item in files_directories:
        if item == file_name:
            return True
        
    return False

class init:
    curr_dir_path = ""
    user = ""
    
    def __init__(self, dir_path):
        self.curr_dir_path = dir_path  # Use self.curr_dir_path to refer to the class attribute
        
        if not isexist(".drvl",self.curr_dir_path): 
            self.user = input("Provide a username: ")
            drvl_makedirs(self.curr_dir_path,self.user)
          
dir_path = os.getcwd()

if len(sys.argv) == 1:
    print_usage_help()
    
elif sys.argv[1] == "init":
    obj = init(dir_path)
    # print(dir_path)
    
elif sys.argv[1]=="add":
    if(isexist(dir_path,sys.argv[2])):
        add_file(sys.argv[2])   
        
    else:
        print("File doesnt exist !!")
        exit()
        
elif sys.argv[1]=="status":
    if(isexist(".drvl",dir_path)==False):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()

    print_status(dir_path)
    
else:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()
