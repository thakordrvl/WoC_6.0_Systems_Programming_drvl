import os
import sys

current_directory_from_CLA = input("Enter Your path: ")
files_and_directories = os.listdir(current_directory_from_CLA)

for item in files_and_directories:
    item_path = os.path.join(current_directory_from_CLA, item)
    if os.path.isfile(item_path):
        size = os.path.getsize(item_path)  # Get size of the file in bytes
        last_modified = os.path.getmtime(item_path)  # Get last modification time
        print(f"File: {item}, Size: {size} bytes, Last Modified: {last_modified}")
        

