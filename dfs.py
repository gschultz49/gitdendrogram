#!/usr/bin/python

# Notes
# Use this on the root of a folder
# The git is what slows this down for the most part...

import os
from glob import glob
import json
import subprocess

global options
# Default options
options= {
  "git": "false"
  # "git": "true"
}

# Dictate path here, maybe make this a CL arguement later
root="C:\Users\GSCHULTZ\Desktop\SimulScan"  
# root ="C:\Users\GSCHULTZ\Desktop\gitstats-new"
# root="C:\Users\GSCHULTZ\Desktop\gitdendrogram\\top"


def appendRoot(root,arr):
  ''' Dictates and appends json data SPECIFICALLY for the root folder.

  Args:
    root (str): Full system path to target directory
    arr (list): Contains all jsons of type Root

  '''
  arr.append({
    "name": root,
    "parent": "null",
    "children" : DFR(root),
    "isFile" : "false",
  })
  return (arr)

def getParentDirectory():
  reference=os.getcwd()
  os.chdir('..')
  parent=os.getcwd()
  os.chdir(reference)
  return parent

def appendFile(file, parent, arr):
  '''Dictates and appends json data SPECIFICALLY for any file

  Args:
    file (str): File name with extension, ex: foo.txt
    parent (str): Full path to parent directory of this file
    arr (list): Contains all jsons of type file at this level

  '''

  # Saves output of CL call to variable for storage to json
  global local_root

  


  potential_parent=getParentDirectory()
  # special case for files in root directory
  if os.path.relpath(potential_parent,parent)==os.path.basename(local_root):
    parent=potential_parent
  

  full_file_path= os.path.join(parent,file)
  git_path= os.path.relpath(full_file_path, local_root)

  # print (parent,file, os.getcwd())




  global options
  if options['git']=="true":
    # gets all commit data across branches for this file
    commit_data = str(subprocess.check_output("cd %s && git log --all -- \"%s\" && cd %s" %(parent,file, reference), shell=True))
    if commit_data=="":
      commit_data="No data available"
  else:
    commit_data="Git mode not enabled"
  

  



  arr.append({
      "name" : file,
      "parent" : parent,
      "commit_data" : commit_data,  
      "isFile": "true",
      "full_path": full_file_path,
      "git_path": git_path
  })
  return (arr)

def appendDir(direct, parent, dir_path, parent_simple, new_dir_path,arr):
  '''Dictates and appends json data SPECIFICALLY for any directory

  Args:
    direct (str): Directory name, dependent on OS can be directory\ (Windows) or directory/ (Linux)
    parent (str): Full path to parent directory of this directory
    dir_path (str): Full system path to this directory, can vary between Windows/Linux
    parent_simple (str): Simple name of parent directory, without slashes
    new_dir_path (str): Joined path of this directory and root
    arr (list): arr (list): Contains all jsons of type directory at this level

  '''
  arr.append({
     "name": direct,
     "file_path":dir_path,
     "parent":parent,
     "parent_simple":parent_simple,
     "new_dir_path": new_dir_path,
     "children": DFR(new_dir_path),
     "isFile": "false",
  })
  return arr



def generateFile(files, parent):
  '''Returns jsons for all files at this directory

  Args:
    files (list): Contains names with extensions of all files in this directory, ex : ['foo.txt','bar.pdf'] 
    parent (str): Full path to parent directory of this file

  '''

  keeper=[]
  for file in files:
    keeper=appendFile(file,parent,keeper)

  return keeper

def generateDirs(dirs, parent, abs_path):
  '''Returns jsons for all directories within the current directory

    Args:
      dirs (list): Contains names of all directories within this directory, ex : ['dir1','dir2'] 
      parent (str): Full path to parent directory of this directory
      abs_path (str): the full path to the root of the target repo

  '''

  master=[]
  for direct in dirs:
    new_dir_path=os.path.join(abs_path,direct)
    file_dir= os.path.dirname(new_dir_path)
    parent = os.path.dirname(file_dir)
    parent_simple= os.path.split(os.path.dirname(file_dir))[-1]

    master=appendDir(direct,parent, file_dir, parent_simple, new_dir_path,master)


  return master

def DFR(abs_path, master=[]):
  '''Recursively enables the generation of directories and files, returns the relevant json data

  Args:
    abs_path (str): the full path to the root of the target repo
    master (list): contains total json structure of this repo   

  '''

  # Setup, needed regardless of recursion state
  root=os.chdir(abs_path)
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # Base case, indicates endpoints
  if dirs!=[] or file!=[]:
    # construct json data for files and directories
    master=  generateDirs(dirs, parent, abs_path) + generateFile(files, parent) 

  return master
  
def outputData(root,final_output):
  '''Sets up and writes the json data to <root_path>/TREE_OUTPUT/<root>.json

  Args:
    root (str): Full system path to target directory
    final_output (list): full json data for this root directory

  '''

  new_dir= root+"/"+"TREE_OUTPUT"

  os.chdir(root)

  # check if new directory exists and move into it, else make it
  os.chdir(new_dir) if os.path.exists(new_dir) else os.mkdir(new_dir)

  output_name=os.path.basename(root)

  # directs output to <root_path>/TREE_OUTPUT/<root_basename>.json
  with open(new_dir+'/'+output_name+'.json', 'w') as outfile:
    # Pretty output for file
    json.dump(final_output[0], outfile, indent=4, sort_keys=False, separators=(',', ': '))


  # Uncomment to output into terminal
  # print ("final_output %s" %(json.dumps(final_output, indent=4, sort_keys=True)))

def start(root):
  '''Kicks off execution

  Args: 
     root (str): Full system path to target directory
  '''
  
  # inital root setup and start the first recursive call
  # final_output=[]
  final_output=appendRoot(root,[])

  # output data 
  outputData(root,final_output)



if __name__ == '__main__':
  global local_root 
  local_root=root
  start(root)
