#!/usr/bin/python

import os
from glob import glob
import json

# if is directory, should have children

# ideally...
treeData =[
  {
      "name": "top",
      "parent": "null",
      "children": [
        {
          "name": "second",
          "parent": "top",
          "children": [
            {
              "name": "third",
              "parent": "second",
              "children" : [
                {
                    "name": "thirdfile.txt",
                    "parent": "third"
                }
              ]
            },
            {
              "name": "fourth",
              "parent": "second",
              "children" : [
                {
                    "name": "fourthfile.txt",
                    "parent": "fourth"
                }
              ]
            }
          ]
        },

        {
          "name": "second2",
          "parent": "top",
          "children" : [
            {
                "name" : "second2file.txt",
                "parent": "second2"
            }
          ]
        }
      ]
  }
]

# ex: /Users/gschultz49/Desktop/Projects/dfs/top


def directDFS(abs_path):
  print (abs_path)

  root=os.chdir(abs_path)
  # python3, linux way 
  # dirs = next(os.walk(root))[1]
   # files = [f for f in os.listdir(root) if os.path.isfile(f)]
   # name=abs_path[abs_path.rfind("/")+1:]

  # glob is pretty cool
  dirs = glob('*/')
  files = glob('*.*')
  parent= os.path.dirname(abs_path)
  folder_name = os.path.basename(abs_path)

  # print ("\n Directories: %s\n Files : %s\n folder_path: %s\n folder_name: %s\n parent_path: %s" %(dirs, files, folder_name, abs_path, parent))
  print ("\n Current Folder: %s\n Directories: %s\n Files: %s\n" %(abs_path, dirs, files))

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

final=[]
final.append({
  "name": root,
  "parent": "null",
  "children" : directDFS(root)
  })
# final.append(directDFS(root))



# for reset
os.chdir(root)

print ("Final %s" %(json.dumps(final, indent=4, sort_keys=True)))

with open('data.json', 'w') as outfile:
    # pretty output
    json.dump(final, outfile, indent=4, sort_keys=True, separators=(',', ': '))