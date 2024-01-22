import os
import hashlib
import shutil
import json
import sys

class init:
    
    def __init__(self, dir_path):
        print(dir_path)
    
if len(sys.argv) > 2 or len(sys.argv)==1:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()
    
elif sys.argv[1]=="init":
    dir_path = os.getcwd()
    obj = init(dir_path)
    
else:
    print("Invalid CLA, Exiting program, Kindly recompile")
    exit()
    