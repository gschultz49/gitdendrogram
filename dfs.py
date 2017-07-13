#!/usr/bin/python

# Notes
# Use this on the root git directory directory
# This is currently very slow for huge directories

import os
from glob import glob
import json
import subprocess

# Dictate path here, make this a CL arguement later
root= "C:\\Users\\GSCHULTZ\\Desktop\\gitdendrogram\\top"
# root= "C:\Users\GSCHULTZ\Desktop\gitstats-new\gitstats\Flask"

# Loops through all files and generates the corresponding JSON data

def generateFile(files, parent):
  keeper=[]
  for file in files:
    # saves output of CL call to variable for storage to json
    commit_data = subprocess.check_output("git log --follow %s" %(file), shell=True)
    keeper.append({
      "name" : file,
      "parent" : parent,
      "commit_data" : commit_data,
      "isFile": "true"      
    })
  return keeper



def directDFS(abs_path, master=[]):
  # Setup, needed regardless of recursion state
  root=os.chdir(abs_path)
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # NOT NEEDED   Base Case, generates json directories of purely files
  # if dirs==[]:
  # 	return generateFile(files, parent)


  # Base case
  # generates json for directories containing files AND directories
  if files!=[]:
    master= generateFile(files, parent)

  # enters directory
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
  	  })

  return master
	


# inital root setup and recursive call
final=[]
final.append({
  "name": root,
  "parent": "null",
  "children" : directDFS(root),
  "isFile" : "false",
  })

# reset for json dump
os.chdir(root)

# Output to terminal
print ("Final %s" %(json.dumps(final, indent=4, sort_keys=True)))

# pretty output for file
with open('data.json', 'w') as outfile:
	# write ONLY the json, not the array
	json.dump(final[0], outfile, indent=4, sort_keys=True, separators=(',', ': '))