import os
import hashlib
import shutil
import json
import sys
from datetime import datetime
import platform
import numpy as np
import base64

dir_path = os.getcwd()
universal_drvl_path = ""

def remove_from_json(json_path):
    try:
        with open(json_path, "w") as json_file:
            json_file.write("{}")
        # print(f"Content of '{json_path}' successfully removed.")
    except FileNotFoundError:
        print(f"Error: File '{json_path}' not found.")
        exit()

def append_to_json(json_path, key, value):
    try:
        # Create the directory structure if it doesn't exist
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        if os.path.exists(json_path):
            with open(json_path, "r") as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = {}
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

def extract_universal_drvl_path(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "universal_drvl_path:" in line:
                    path = line.split("universal_drvl_path:")[1].strip()
                    return path

            print(f"Error: 'universal_drvl_path:' not found in '{file_path}'.")
            return None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

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

def add(to_file_name, file_path):
        
    dir_path = os.getcwd()
    files_directories = os.listdir(dir_path)    
    file_name = to_file_name
    
    if(file_name=="main.py"):
        return
    
    drvl_path = os.path.join(dir_path,".drvl")
    
    if ".drvl" not in files_directories:
        drvl_path = universal_drvl_path
    
    index_path = os.path.join(drvl_path, "branches", "main", "index.json")
    added_path = os.path.join(drvl_path, "branches", "main", "added.json")
    md5_hash = compute_md5(file_path)
    append_to_json(index_path, file_name, {"md5 hash": md5_hash})
    append_to_json(added_path, file_name, {"md5 hash": md5_hash, "file_path": file_path})
    print(f"File '{file_name}' successfully added to the repository.")

def addallfiles(dir_path, flag):
    files_directories = os.listdir(dir_path)
    if '.drvl' not in files_directories and flag==False:
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
    
    for item in files_directories:
        
        full_path = os.path.join(dir_path,item)
        # print(full_path)

        if os.path.isdir(full_path) and item != '.drvl' and item!='.git':
            addallfiles(full_path,True)
            
        elif item!='.drvl' and item!='.git':
            add(item,full_path)  
  
def encode_file_content_to_base64(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return base64.b64encode(binary_data).decode('utf-8')      

def get_all_files(dir_path, all_files):
    temp_all_files = os.listdir(dir_path)

    for item in temp_all_files:
        item_path = os.path.join(dir_path, item)

        if os.path.isfile(item_path):
            all_files.append(item_path)
        elif os.path.isdir(item_path) and item!=".git" and item!=".drvl":
            get_all_files(item_path, all_files)

def get_tracked_hashes(dir_path):
    json_path = os.path.join(dir_path, ".drvl/branches/main/added.json")
    
    try:
        with open(json_path, "r") as added_file:
            added_data = json.load(added_file)
            tracked_hashes = [file_info["md5 hash"] for file_info in added_data.values()]
            return tracked_hashes
    except FileNotFoundError:
        return []

def get_untracked_files(dir_path):
    tracked_hashes = get_tracked_hashes(dir_path)
    all_files = []
    get_all_files(dir_path, all_files)

    untracked_files = []

    for file_path in all_files:
        file_hash = compute_md5(file_path)
        base_name = os.path.basename(file_path)
        if file_hash not in tracked_hashes and base_name != "main.py":
            # Include folder name to avoid confusion with same-named files in different folders
            folder_name = os.path.dirname(file_path)
            untracked_files.append(os.path.join(os.path.basename(folder_name), base_name))

    return untracked_files 
     
def decode_and_update_files(commit, destination_folder):
    
    base_path = os.getcwd()
    
    files = commit.get("files", [])
    for file_data in files:
        filename = file_data.get("filename")
        encoded_content = file_data.get("encoded_content")
        file_path = file_data.get("file_path")

        try:
            decoded_content = base64.b64decode(encoded_content)
            relative_path = os.path.relpath(file_path,base_path)
            destination_path = os.path.join(destination_folder, filename)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            with open(destination_path, 'wb') as file:
                file.write(decoded_content)

            print(f"File '{filename}' updated/copied.")
        except (PermissionError, FileNotFoundError) as e:
            print(f"Error updating/copying file '{filename}': {str(e)}")
        except Exception as e:
            print(f"Unexpected error updating/copying file '{filename}': {str(e)}")
            
def commits(base_directory, message):
    drvl_path = os.path.join(base_directory, ".drvl")
    added_path = os.path.join(drvl_path, "branches", "main", 'added.json')
    commits_path = os.path.join(drvl_path, 'objects', 'commits.json')
      
    if not os.path.exists(added_path):
        print("Files have not been tracked yet. Use the add command to track files. After that, you can use the commit command.")
        exit()
        
    commits = []
    if os.path.exists(commits_path):
        with open(commits_path, 'r') as commits_file:
            commits = json.load(commits_file)
        
    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)
        
    users_file_path = os.path.join(drvl_path, "branches", "main", "users")
    
    if not os.path.exists(users_file_path):
        print("Users.txt file doesn't exist. Kindly restore it back to proceed further.")
        exit()
        
    username = extract_username_from_file(users_file_path)
    
    commit = {
        "timestamp": datetime.utcnow().isoformat(),
        "user-name": username, 
        "message": message,
        "date": datetime.utcnow().strftime("%d-%m-%Y"),
        "files": []
    }
    
    for filename, file_info in added_data.items():
        file_path = file_info.get("file_path")
        if os.path.exists(file_path):
            actual_md5 = compute_md5(file_path)

            if actual_md5 == file_info.get("md5 hash") or filename == "main.py":
                encoded_content = encode_file_content_to_base64(file_path)
                commit["files"].append({"filename": filename, "file_path": file_path, "encoded_content": encoded_content})
            else:
                print(f"Warning: File '{filename}' has changed. Kindly use the Add command first.")
                exit()
        else:
            print(f"Warning: File '{filename}' not found. Kindly use the Add command first.")
            exit()

    commits.append(commit)
    with open(commits_path, 'w') as commits_file:
        json.dump(commits, commits_file, indent=2)
        commits_file.write('\n')
        
    print("Commit Successful")
    
def remove_commit(commits_path):
    if not os.path.exists(commits_path):
        print("Error: 'commits.json' not found.")
        return None
    
    with open(commits_path, 'r') as commits_file:
        commits = json.load(commits_file)
        
    if not commits:
        print("Error: No commits to remove.")
        return None

    removed_commit = commits.pop()
    
    if not commits:
        print("Error: No commit left after removal.")
        return None
    
    commit_before_removed = commits[-1]

    with open(commits_path, 'w') as commits_file:
        json.dump(commits, commits_file, indent=2)

    print("Commit removed successfully:")

    return commit_before_removed
    
def rmcommit(dir_path):
    commits_path = os.path.join(dir_path,".drvl","objects","commits.json")
    
    if(os.path.exists(commits_path)==False):
        print("The path of commits.json has been changed. Kindly check if the file exists and it is placed in correct folder")
    
    to_be_restore = remove_commit(commits_path)
    
    if(to_be_restore):
        decode_and_update_files(to_be_restore,dir_path)

def rmadd(base_directory):
    drvl_path = os.path.join(base_directory, ".drvl")
    added_path = os.path.join(drvl_path, "branches", "main", "added.json")
    index_path = os.path.join(drvl_path, "branches", "main", "index.json")

    if not os.path.exists(added_path):
        print("Files have not been tracked yet or added.json doesnt exist. Use add command to track files and create added.json.")
        exit()
        
    remove_from_json(added_path)
    # remove_from_json(index_path)
    print("All files successfully removed from tracking.")
            
def print_status(dir_path):
    untracked_files = get_untracked_files(dir_path)

    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            file_name, folder_name = os.path.splitext(file)[0], os.path.dirname(file)
            print(f"- {file_name} from {folder_name}")
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

def push(base_directory, destination_path):
    drvl_path = os.path.join(base_directory, ".drvl")
    commits_path = os.path.join(drvl_path, 'objects', 'commits.json')

    if not os.path.exists(commits_path):
        print("No commits found. Use commit command to commit changes.")
        exit()

    with open(commits_path, 'r') as commits_file:
        commits = json.load(commits_file)

    if not commits:
        print("No commits found. Use commit command to commit changes.")
        exit()

    last_commit = commits[-1]
    if decode_and_update_files(last_commit,destination_path):
        print("commits successfully copied to destination folder")
        exit()

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
            file.write(f"User:{user_name}\n")
            file.write("universal_drvl_path: " + os.getcwd())
            file.write("\n\n")
            
if len(sys.argv) == 1:
    print_usage_help()
    
elif sys.argv[1] == "init": 
    obj = init(dir_path)
    # print(dir_path)
    
elif sys.argv[1]=="status":
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
        
    if len(sys.argv)>2:
        print("wrong synyax for status. kindly recompile")
        exit()
        
    universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
    print_status(dir_path)
    
elif sys.argv[1]=="add":
    
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
    
    if len(sys.argv)<=2:
        print("File Name not given")
        exit()
        
    elif sys.argv[2]=='.':
        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
        addallfiles(dir_path,False)
        
    else:
        file_path = os.path.join(dir_path,sys.argv[2])
        
        if os.path.exists(file_path)==False:
            print("File doesnt exist or File name not given!!")
            exit()
            
        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
        add(sys.argv[2],file_path)   
        
elif sys.argv[1] == "commit":
    
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
    
    if len(sys.argv) > 3 and sys.argv[2] == "-m":
        
        commit_message = sys.argv[3]
        flag1 = False
        
        for i in commit_message:
            if i!=' ':
                flag1 = True
                
        if flag1==False:
            print("Cannot commit with empty message kindly recompile")
            exit()
            
        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
        commits(dir_path,commit_message)
        
    else:
        print("Invalid commit command. Use 'commit -m \"message\"'.")
        exit()
        
elif sys.argv[1]=="rmcommit":
    
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
        
    if len(sys.argv)>2:
        print("wrong synyax for status. kindly recompile")
        exit()
        
    universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
    rmcommit(dir_path)
    
    
elif sys.argv[1]=="rmadd":
    
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
        
    if len(sys.argv)>2:
        print("wrong synyax for status. kindly recompile")
        exit()
        
    universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
    rmadd(dir_path)
    
elif sys.argv[1]=="push":
    
    if not os.path.exists(dir_path + "/.drvl"):
        print("Exiting program, This folder has not been intialized/ .drvl doesnt exist, Use init command to intialize ")
        exit()
        
        
    if len(sys.argv)>3 or len(sys.argv)<=2:
        print("wrong synyax for status. kindly recompile")
        exit()
        
    if not os.path.exists(sys.argv[2]):
        print("Destination does not exist. Kindly recompile")
        exit()
    
    dest_path = sys.argv[2]
    universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path,".drvl","branches","main","users"))
    push(dir_path,dest_path)
               
else:
    print("Invalid command, Exiting program, Kindly recompile")
    exit()
    


