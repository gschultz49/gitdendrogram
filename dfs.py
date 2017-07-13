#!/usr/bin/python

import os
from glob import glob
import json


def directDFS(abs_path):
  print (abs_path)

  root=os.chdir(abs_path)

  # glob is pretty cool
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # print ("\n Current Folder: %s\n Directories: %s\n Files: %s\n" %(abs_path, dirs, files))

  if dirs==[]:
    keeper=[]
    for file in files:
      keeper.append({
          "name" : file,
          "parent" : parent     
        })
    return keeper

  master=[]
  for direct in dirs:
    new_dir_path=os.path.join(abs_path,direct)
    current_dir= os.path.dirname(new_dir_path)
    parent = os.path.dirname(current_dir)

    master.append({
        "name" : direct,
        "dir_path" : current_dir,
        "parent": parent,
        "children"  : directDFS(new_dir_path)
      })
  return master
    


# Dictate path heere
root= "C:\\Users\\GSCHULTZ\\Desktop\\gitdendrogram\\top"

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
    json.dump(final, outfile, indent=4, sort_keys=True, separators=(',', ': '))