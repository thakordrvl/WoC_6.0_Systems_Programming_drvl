import os
import hashlib
import shutil
import json
import sys
import datetime
import platform

def write_json(json_path, data):
    try:
        with open(json_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {}

    # Merge existing data with new data
    existing_data.update(data)

    with open(json_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=2)
        
def read_json(json_path):
    try:
        with open(json_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

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
    
def isexist(file_name, path):
    files_directories = os.listdir(path)
    
    for item in files_directories:
        if item == file_name:
            return True
        
    return False    

class add:
    def __init__(self, to_file_name):
        # self.repo_number = input("Please provide the repo_number you want to add in: ")
        self.file_name = to_file_name
        self.file_path = os.path.join(os.getcwd(), self.file_name)
        self.drvl_path = os.getcwd() + "/.drvl"

        # if not os.path.exists(self.repo_path):
        #     print("Repository does not exist")
        #     exit()

        self.index_path = os.path.join(self.drvl_path, "branches", "main", "index.json")
        self.added_path = os.path.join(self.drvl_path, "branches", "main", "added.json")
        md5_hash = compute_md5(self.file_path)

        # Update index.json
        index_data = read_json(self.index_path)
        index_data[self.file_name] = {"md5 hash": md5_hash}
        write_json(self.index_path, index_data)

        # Update added.json
        added_data = read_json(self.added_path)
        added_data[self.file_name] = {"md5 hash": md5_hash}
        write_json(self.added_path, added_data)

        print(f"File '{self.file_name}' successfully added to the repository.")
        
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

class init:
    def __init__(self, dir_path):
        self.curr_dir_path = dir_path
        self.user = ""

        if not os.path.exists(os.path.join(self.curr_dir_path, ".drvl")):
            self.user = input("Provide a username: ")
            self.drvl_makedirs(self.curr_dir_path, self.user)

    def drvl_makedirs(self, base_path, user_name):
        drvl_path = os.path.join(base_path, ".drvl")
        os.makedirs(drvl_path)

        if platform.system() == 'Windows':
            attrib_cmd = f'attrib +h "{drvl_path}"'
            os.system(attrib_cmd)
            
        branches_path = os.path.join(drvl_path, "branches")
        objects_path = os.path.join(drvl_path, "objects")
        os.makedirs(branches_path)
        os.makedirs(objects_path)

        main_branch_path = os.path.join(branches_path, "main")
        os.makedirs(main_branch_path)
        user_txt_path = os.path.join(main_branch_path, "users")
        current_date_time = datetime.datetime.now()

        with open(user_txt_path, "w") as file:
            file.write(f"Date: {current_date_time.strftime('%Y-%m-%d')}\n")
            file.write(f"Timestamp: {current_date_time.strftime('%H:%M:%S')}\n")
            file.write("User: " + user_name)
            file.write("\n\n")
            
dir_path = os.getcwd()

if len(sys.argv) == 1:
    print_usage_help()
    
elif sys.argv[1] == "init":
    obj = init(dir_path)
    # print(dir_path)
    
elif sys.argv[1]=="status":
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()

    print_status(dir_path)
    
elif sys.argv[1]=="add":
    
    # file_path = os.path.join(dir_path,sys.)
    
    if len(sys.argv)<=2:
        print("File Name not given")
        exit()
    
    if os.path.exists(os.path.join(dir_path,sys.argv[2]))==False:
        print("File doesnt exist or File name not given!!")
        exit()
        
    else:
        add(sys.argv[2])   
else:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()
