#!/usr/bin/python

# Notes
# Use this on the root git directory directory

import os
from glob import glob
import json
import subprocess

# Dictate path here, make this a CL arguement later
# root= "C:\\Users\\GSCHULTZ\\Desktop\\gitdendrogram"
root= "C:\Users\GSCHULTZ\Desktop\gitstats-new\gitstats\Flask"


def directDFS(abs_path):
  # Setup, needed regardless of recursion state
  root=os.chdir(abs_path)
  # glob is pretty cool
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # Base Case
  if dirs==[]:
	keeper=[]
	# triggers on NON DIRECTORIES
	for file in files:
	  # saves output of CL call to variable for storage to json
	  commit_data = subprocess.check_output("git log --follow %s" %(file), shell=True)
	  keeper.append({
		  "name" : file,
		  "parent" : parent,
		  "commit_data" : commit_data      
		})
	return keeper

  master=[]
  # triggers on DIRECTORIES
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
		"children"  : directDFS(new_dir_path)
	  })
  return master
	


# inital parent setup

final=[]
final.append({
  "name": root,
  "parent": "null",
  "children" : directDFS(root)
  })

# for reset
os.chdir(root)

# check if it's right
print ("Final %s" %(json.dumps(final, indent=4, sort_keys=True)))

 # pretty output
with open('data.json', 'w') as outfile:
	# write ONLY the json, not the array
	json.dump(final[0], outfile, indent=4, sort_keys=True, separators=(',', ': '))