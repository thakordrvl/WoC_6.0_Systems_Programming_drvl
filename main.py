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
        return

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

def extract_username_from_file(dir_path):
    
    file_path = os.path.join(dir_path,".drvl","branches","main","users")
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "User:" in line:
                    username = line.split("User:")[1].strip()
                    return username

            # print(f"Error: 'User:' not found in '{file_path}'.")
            return None
    except FileNotFoundError:
        # print(f"Error: File '{file_path}' not found.")
        return None

def change_user_name(dir_path, new_username):
    
    file_path = os.path.join(dir_path,".drvl","branches","main","users")
    old_user = extract_username_from_file(file_path)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if "User:" in line:
                line = line.replace(line.split("User:")[1].strip(), new_username)
            file.write(line)

    print(f"Username changed to '{new_username}' in users.txt.")
    
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
        return
    
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
    md5_hash_path = os.path.join(drvl_path, 'objects', 'files_md5_hash.json')
    
    if not os.path.exists(added_path):
        print("Files have not been tracked yet. Use the add command to track files. After that, you can use the commit command.")
        return

    # Create an empty MD5 hash dictionary if the file doesn't exist
    md5_hash_data = {}
    if os.path.exists(md5_hash_path):
        with open(md5_hash_path, 'r') as md5_hash_file:
            md5_hash_data = json.load(md5_hash_file)
    
    commits = []
    
    if os.path.exists(commits_path):
        with open(commits_path, 'r') as commits_file:
            commits = json.load(commits_file)
        
    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)
        
    users_file_path = os.path.join(drvl_path, "branches", "main", "users")
    
    if not os.path.exists(users_file_path):
        print("Users.txt file doesn't exist. Kindly restore it back to proceed further.")
        return
        
    username = extract_username_from_file(users_file_path)
    
    commit = {
        "timestamp": datetime.utcnow().isoformat(),
        "user-name": username, 
        "message": message,
        "date": datetime.utcnow().strftime("%d-%m-%Y"),
        "commit_hash": None,  # Placeholder for the commit-specific hash
        "files": []
    }

    # Calculate a unique MD5 hash for this commit based on timestamp and files
    commit_hash_input = f"{commit['timestamp']}:{json.dumps(commit['files'], sort_keys=True)}"
    commit_hash = hashlib.md5(commit_hash_input.encode()).hexdigest()
    commit["commit_hash"] = commit_hash
    
    for filename, file_info in added_data.items():
        file_path = file_info.get("file_path")
        if os.path.exists(file_path):
            actual_md5 = compute_md5(file_path)
            
            if actual_md5 == md5_hash_data.get(file_path):
                print(f"No changes made to file '{filename}'. Skipping.")
                continue
            
            if actual_md5 == file_info.get("md5 hash") or filename == "main.py":
                encoded_content = encode_file_content_to_base64(file_path)
                commit["files"].append({"filename": filename, "file_path": file_path, "encoded_content": encoded_content})
                md5_hash_data[file_path] = actual_md5  # Update the MD5 hash in the dictionary
            else:
                print(f"Warning: File '{filename}' has changed. Kindly use the Add command first.")
                return
        else:
            print(f"Warning: File '{filename}' not found. Kindly use the Add command first.")
            return

    # Check if commit has files before appending it to commits
    if commit["files"]:
        commits.append(commit)
    
        with open(commits_path, 'w') as commits_file:
            json.dump(commits, commits_file, indent=2)
            commits_file.write('\n')

        print("Commit Successful")
    else:
        print("No changes made. Commit skipped.")

    with open(md5_hash_path, 'w') as md5_hash_file:
        json.dump(md5_hash_data, md5_hash_file, indent=2)
        md5_hash_file.write('\n')
        
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
        return
    
    to_be_restore = remove_commit(commits_path)
    
    if(to_be_restore):
        decode_and_update_files(to_be_restore,dir_path)

def rmadd(base_directory):
    drvl_path = os.path.join(base_directory, ".drvl")
    added_path = os.path.join(drvl_path, "branches", "main", "added.json")
    index_path = os.path.join(drvl_path, "branches", "main", "index.json")

    if not os.path.exists(added_path):
        print("Files have not been tracked yet or added.json doesnt exist. Use add command to track files and create added.json.")
        return
        
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
        return

    with open(commits_path, 'r') as commits_file:
        commits = json.load(commits_file)

    if not commits:
        print("No commits found. Use commit command to commit changes.")
        return

    last_commit = commits[-1]
    if decode_and_update_files(last_commit,destination_path):
        print("commits successfully copied to destination folder")
        return

class init:
    def __init__(self, dir_path):
        self.curr_dir_path = dir_path
        self.user = ""

        if not os.path.exists(os.path.join(self.curr_dir_path, ".drvl")):
            self.user = input("Provide a username: ")
            self.drvl_makedirs(self.curr_dir_path, self.user)
            print(".drvl created successfully")
            
        else:
            print("This folder has already been intialised once")

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

while True:
    user_input = input("Enter command: ")
    
    if not user_input:
        continue
    
    args = user_input.split()
    print(args)
    
    if args[0] == "exit":
        print("Exiting program.")
        break
    
    if args[0]=="help":
        if len(args) > 1:
            print("wrong syntax for help. Kindly recompile")
            continue
        
        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
        print_usage_help()
        
    elif args[0] == "init":
        if len(args) > 1:
            print("wrong syntax for help. Kindly recompile")
            continue
        
        init(dir_path)
        
    elif args[0] == "status":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue
        
        if len(args) > 1:
            print("Wrong syntax for status. Kindly recompile.")
            continue
        
        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
        print_status(dir_path)
    
    elif args[0] == "add":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue
        
        if len(args) > 2:
            print("wrong syntax for add command")
            continue

        if len(args) <= 1:
            print("File Name not given")
            continue

        elif args[1] == '.':
            universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
            addallfiles(dir_path, False)

        else:
            file_path = os.path.join(dir_path, args[1])

            if not os.path.exists(file_path):
                print("File doesn't exist or File name not given!!")
                continue

            universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
            add(args[1], file_path)
     
    elif args[0] == "commit":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue

        if len(args) > 3 and args[1] == "-m":
            if args[2][0] == '"' and args[-1][-1] == '"':
                commit_message = " ".join(args[2:])
                commit_message = commit_message[1:-1]  # Remove the leading and trailing quotes
                universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
                commits(dir_path, commit_message)
            else:
                print("Invalid commit command. Use 'commit -m \"message\"'.")
                continue
        else:
            print("Invalid commit command. Use 'commit -m \"message\"'.")
            continue

    elif args[0] == "rmcommit":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue

        if len(args) > 1:
            print("Wrong syntax for rmcommit. Kindly recompile.")
            continue

        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
        rmcommit(dir_path)

    elif args[0] == "rmadd":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue

        if len(args) > 1:
            print("Wrong syntax for rmadd. Kindly recompile.")
            continue

        universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
        rmadd(dir_path)

    elif args[0] == "push":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue

        if len(args) == 2:
            if args[1][0] == '"' and args[1][-1] == '"':
                dest_path = args[1][1:-1]  # Remove the leading and trailing quotes
                universal_drvl_path = extract_universal_drvl_path(os.path.join(dir_path, ".drvl", "branches", "main", "users"))
                push(dir_path, dest_path)
            else:
                print("Invalid push command. Destination should be enclosed in double quotes.")
                continue
        else:
            print("Wrong syntax for push. Kindly recompile.")
            continue
        
    elif args[0] == "user" and len(args)>=2 and args[1]=="show":
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue

        if len(args) == 2 and args[1] == "show":
            user = extract_username_from_file(dir_path)
            print(f"user : {user}")
            
        else:
            print("Wrong syntax for user. Use 'user show'.")
            continue
        
    elif args[0] == "user" and len(args)>=3 and args[1]=="set":
        
        if not os.path.exists(dir_path + "/.drvl"):
            print("Exiting program, This folder has not been initialized/ .drvl doesn't exist, Use init command to initialize ")
            continue
        
        if not os.path.exists(os.path.join(dir_path,".drvl","branches","main","users")):
            print("Error. The users.txt file has been deleted or has been moved. kindly check")
            continue
    
        if len(args) == 3 and args[1] == "set":
            username = args[2]
            change_user_name(dir_path, username)
            
        else:
            print("Wrong syntax for user set. Use 'user set <username>'.")
            continue
    
    else:
        print("Invalid command. Please try again.")
    