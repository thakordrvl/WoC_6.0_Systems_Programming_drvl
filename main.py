import os
import hashlib
import shutil
import json
import sys
from datetime import datetime
import platform
import numpy as np
import base64
        
def append_to_json(json_path, key, value):
    try:
        with open(json_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {}

    # Append or update the value for the specified key
    existing_data[key] = value

    with open(json_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=2)

def compute_md5(file_path):
    initial_chunk_size = 4096
    max_chunk_size = 65536
    hash_md5 = hashlib.md5()
    chunk_size = initial_chunk_size

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_md5.update(chunk)
                if chunk_size < max_chunk_size:
                    chunk_size *= 2
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except PermissionError:
        print(f"Permission error. Check file permissions: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return hash_md5.hexdigest()

def add(to_file_name):
        
    dir_path = os.getcwd()
    files_directories = os.listdir(dir_path)
    
    if '.drvl' not in files_directories:
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
    
    file_name = to_file_name
    file_path = os.path.join(os.getcwd(), file_name)
    drvl_path = os.getcwd() + "/.drvl"
    index_path = os.path.join(drvl_path, "branches", "main", "index.json")
    added_path = os.path.join(drvl_path, "branches", "main", "added.json")
    md5_hash = compute_md5(file_path)
    append_to_json(index_path, file_name, {"md5 hash": md5_hash})
    append_to_json(added_path, file_name, {"md5 hash": md5_hash})
    print(f"File '{file_name}' successfully added to the repository.")

def extract_username_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "User:" in line:
                    username = line.split("User:")[1].strip()
                    return username

            print(f"Error: 'User:' not found in '{file_path}'.")
            return None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def encode_file_content_to_base64(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return base64.b64encode(binary_data).decode('utf-8')      
    
def commits(base_directory, message):
    drvl_path = os.path.join(base_directory,".drvl")
    index_path = os.path.join(drvl_path,"branches","main",'index.json')
    commits_path = os.path.join(drvl_path, 'objects', 'commits.json')
    print(index_path)
    
    if os.path.exists(drvl_path)==False:
        print("This directory has not been initalised")
        exit()
        
    if os.path.exists(index_path)==False:
        print("Files has not been tracked yet. Use add command to track files, After that you could use commit command")
        exit()
        
    commits = []
    if os.path.exists(commits_path):
        with open(commits_path, 'r') as commits_file:
            commits = json.load(commits_file)
        
    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)
        
    if os.path.exists(os.path.join(drvl_path,"branches","main","users"))==False:
        print("User.txt file doesnt exist kindly restore it back to proceed further")
        exit()
        
    username = extract_username_from_file(os.path.join(drvl_path,"branches","main","users"))
    
    commit = {
        "timestamp": datetime.utcnow().isoformat(),
        "user-name": username, 
        "message": message,
        "date": datetime.utcnow().strftime("%d-%m-%Y"),
        "files": []
    }
    # Update or add files to the commit
    for filename, file_info in index_data.items():
        file_path = os.path.join(base_directory, filename)
        if os.path.exists(file_path):
            actual_md5 = compute_md5(file_path)

            if actual_md5 == file_info.get("md5 hash") or filename=="main.py":
                encoded_content = encode_file_content_to_base64(file_path)
                commit["files"].append({filename: encoded_content})
            else:
                print(f"Warning: File '{filename}' has changed. Kindly Use Add command first.")
                exit()
        else:
            print(f"Warning: File '{filename}' not found. Kindly use Add command first")
            exit()

    # Append the new commit to the array
    commits.append(commit)

# Write the updated commits.json without overwriting existing content
    with open(commits_path, 'w') as commits_file:
        json.dump(commits, commits_file, indent=2)
        commits_file.write('\n')
        
        
    print("Commit Successful")
    

def addallfiles(dir_path):
    files_directories = os.listdir(dir_path)
    if '.drvl' not in files_directories:
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
    
    for item in files_directories:
        
        full_path = os.path.join(dir_path,item)
        # print(full_path)

        if os.path.isdir(full_path) and item != '.drvl' and item!='.git':
            addallfiles(full_path)
            
        elif item!='.drvl' and item!='.git':
            add(item)
            
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
            
        else:
            print("This folder has already been intialised once")
            exit()

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
        current_date_time = datetime.now()

        with open(user_txt_path, "w") as file:
            file.write(f"Date: {current_date_time.strftime('%d-%m-%Y')}\n")
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
        
    elif sys.argv[2]=='.':
        addallfiles(dir_path)
    
    elif os.path.exists(os.path.join(dir_path,sys.argv[2]))==False:
        print("File doesnt exist or File name not given!!")
        exit()
        
    else:
        add(sys.argv[2])   
        
elif sys.argv[1] == "commit":
    if len(sys.argv) > 3 and sys.argv[2] == "-m":
        
        commit_message = sys.argv[3]
        flag1 = False
        
        for i in commit_message:
            if i!=' ':
                flag1 = True
                
        if flag1==False:
            print("Cannot commit with empty message kindly recompile")
            exit()
            
        commits(dir_path,commit_message)
        
    else:
        print("Invalid commit command. Use 'commit -m \"message\"'.")
        exit()
       
else:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()


