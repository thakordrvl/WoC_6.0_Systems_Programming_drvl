import os
import hashlib
import shutil
import json
import sys
import datetime
import platform

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
        
def isexist(path):
    files_directories = os.listdir(path)
    
    for item in files_directories:
        if item == ".drvl":
            return True
        
    return False

class init:
    curr_dir_path = ""
    user = ""
    
    def __init__(self, dir_path):
        self.curr_dir_path = dir_path  # Use self.curr_dir_path to refer to the class attribute
        
        if not isexist(self.curr_dir_path): 
            self.user = input("Provide a username: ")
            drvl_makedirs(self.curr_dir_path,self.user)

if len(sys.argv) == 1:
    print_usage_help()
    
elif sys.argv[1] == "init":
    dir_path = os.getcwd()
    obj = init(dir_path)
    print(dir_path)
    
else:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()
