import os
import sys
import json
import subprocess
from glob import glob


assert (len(sys.argv) >1), "\n\nEnter target directory path as an arguement\n"

root=sys.argv[1]

global options
options= {
  "git": "true",
  "compressed": "false",
  "terminal_output": "false"
}


def start(root):
  '''Kicks off execution

  Args: 
     root (str): Full system path to target directory
  '''
  print ("Building JSON...")
  # inital root setup and start the ecursive call
  final_output=appendRoot(root,[])

  # output data 
  outputData(root,final_output)

def appendRoot(root,arr):
  '''Dictates and appends json data SPECIFICALLY for the root folder.

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

def DFR(abs_path, master=[]):
  '''Recursively enables the generation of directories and files, returns the 
  relevant json data

  Args:
    abs_path (str): the full path to the target repo
    master (list): data container for json data at `this` directory level   

  '''
  # Setup, needed regardless of recursion state
  root=os.chdir(abs_path)
  dirs = glob('*/')  # array of directories
  files = glob('*.*') # array of files 
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # Base case, indicates endpoints
  if dirs!=[] or files!=[]:
    # construct json data for files and directories
    master = generateDirs(dirs, parent, abs_path) + generateFile(files, parent) 

  return master

def getParentDirectory():
  ''' Returns full path to parent directory'''
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
  global local_root
  global options
  
  potential_parent=getParentDirectory()
  # special case for files in root directory
  if os.path.relpath(potential_parent,parent)==os.path.basename(local_root):
    parent=potential_parent
  
  full_file_path= os.path.join(parent,file)
  git_path= os.path.relpath(full_file_path, local_root)

  reference=os.getcwd()
  
  if options['git']=="true":
    # gets all commit data across branches for this file
    commit_data = str(subprocess.check_output("cd %s && git log --all -- \"%s\" && cd %s" %(parent,file, reference), shell=True).decode('utf-8'))
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
    direct (str): Directory name, dependent on OS can be
     directory\ (Windows) or directory/ (Linux)
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
    files (list): Contains names with extensions of all files in this directory
      ex : ['foo.txt','bar.pdf'] 
    parent (str): Full path to parent directory of this file

  '''
  keeper=[]
  for file in files:
    keeper=appendFile(file,parent,keeper)

  return keeper

def generateDirs(dirs, parent, abs_path):
  '''Returns jsons for all directories within the current directory

    Args:
      dirs (list): Contains names of all directories within this directory
       ex : ['dir1','dir2'] 
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

  
def outputData(root,final_output):
  '''Sets up and writes the json data to <root_path>/TREE_OUTPUT/<root>.json

  Args:
    root (str): Full system path to target directory
    final_output (list): full json data for this root directory

  '''
  new_dir= os.path.join(root, "TREE_OUTPUT")

  os.chdir(root)

  # check if new directory exists and move into it, else make it
  os.chdir(new_dir) if os.path.exists(new_dir) else os.mkdir(new_dir)

  output_name=os.path.basename(root)

  output_file_name=new_dir+'/'+output_name+'.json'

  # directs output to <root_path>/TREE_OUTPUT/<root_basename>.json
  with open(output_file_name, 'w') as outfile:
    # Pretty output if desired
    global options
    if options['compressed']=="true":
      json.dump(final_output[0], outfile)
    else:
      json.dump(final_output[0], outfile, indent=4, sort_keys=False, separators=(',', ': '))
    
  print ("\nData options: %s \nJSON build successful!\n\nData written to \n%s\n" %(json.dumps(options, indent=4, sort_keys=True),output_file_name))
  
  if options['terminal_output']=="true":
    print ("Final Output: %s" %(json.dumps(final_output, indent=4, sort_keys=True)))

global local_root 
local_root=root
start(root)




