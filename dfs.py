#!/usr/bin/python

# Notes
# Use this on the root of a repo
# The git is what slows this down for the most part...

import os
from glob import glob
import json
import subprocess
import hashlib

# Dictate path here, make this a CL arguement later
# root= "C:\\Users\\GSCHULTZ\\Desktop\\gitdendrogram\\top"
# root= "C:\Users\GSCHULTZ\Desktop\gitstats-new\gitstats\Flask"
# root="C:\Users\GSCHULTZ\Desktop\SimulScan"
# root="C:\Users\GSCHULTZ\Desktop\SimulScan\SimulScanTest"
root="/Users/gschultz49/Desktop/Projects/SpringMvcStepByStep"

# Loops through all files and generates the corresponding JSON data

def generateFile(files, parent):
  keeper=[]
  for file in files:
    # badChars = set("&")
    # for char in badChars:
    #   if char in file:
    #     index= file.index(char)
    #     file = file[:index]+"\\"+file[index:]


    # saves output of CL call to variable for storage to json
    # commit_data = subprocess.check_output("git log --follow \"%s\"" %(file), shell=True)
    keeper.append({
      "name" : file,
      "parent" : parent,
      # "commit_data" : str(commit_data),
      "isFile": "true",
      # "id_hash" : int(hashlib.md5(os.path.join(parent+file)).hexdigest(), 16)  
    })
  return keeper


def directDFS(abs_path, master=[]):
  # Setup, needed regardless of recursion state
  root=os.chdir(abs_path)
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

   # enters each directory
  if dirs!=[]:
    master= generateFile(files, parent)
    for direct in dirs:
      new_dir_path=os.path.join(abs_path,direct)
      file_dir= os.path.dirname(new_dir_path)
      parent = os.path.dirname(file_dir)
      parent_simple= os.path.split(os.path.dirname(file_dir))[-1]
      master.append({
        "name" : direct,
        "file_path" : file_dir,
        "parent": parent,
        "parent_simple" : parent_simple,
        "children"  : directDFS(new_dir_path),
        "isFile":"false",
        # "id_hash" : int(hashlib.md5(os.path.join(parent+direct)).hexdigest(), 16) 
        })


  # Base case
  # generates json for directories containing files AND directories
  # if files!=[]:
  #   master= generateFile(files, parent)

 

  return master
	


# inital root setup and start the first recursive call
final_output=[]
final_output.append({
  "name": root,
  "parent": "null",
  "children" : directDFS(root),
  "isFile" : "false",
  # "id_hash" : int(hashlib.md5(os.path.join("null"+root)).hexdigest(), 16) 
  })

# reset for json dump
os.chdir(root)
print (final_output)
# Output to terminal
# print ("final_output %s" %(json.dumps(final_output, indent=4, sort_keys=True)))

# pretty output for file
with open('data.json', 'w') as outfile:
	# write ONLY the json, not the array
	json.dump(final_output[0], outfile, indent=4, sort_keys=True, separators=(',', ': '))