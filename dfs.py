#!/usr/bin/python

import os


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

  root=os.chdir(abs_path)
  # python3 way 
  dirs = next(os.walk(root))[1]
  files = [f for f in os.listdir(root) if os.path.isfile(f)]
  name=abs_path[abs_path.rfind("/")+1:]
  print (name)

  if dirs ==[]:
    return {
      "name" : name
    }
    
  directDFS()


directDFS("/Users/gschultz49/Desktop/Projects/dfs/top/second/fourth")


def generateJSON(abs_path):

  root=os.chdir(abs_path)
  # python3 way 
  dirs = next(os.walk(root))[1]
  files = [f for f in os.listdir(root) if os.path.isfile(f)]


  print ("dirs %s" %(dirs))
  print ("files %s" %(files))


# generateJSON("/Users/gschultz49/Desktop/Projects/dfs/top/second/fourth")



# graph = {'A': set(['B', 'C']),
#          'B': set(['A', 'D', 'E']),
#          'C': set(['A', 'F']),
#          'D': set(['B']),
#          'E': set(['B', 'F']),
#          'F': set(['C', 'E'])}


# def dfs(graph, start, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(start)
#     # print (graph[start])
#     for next in graph[start] - visited:
#         dfs(graph, next, visited)
#     return visited

# print(dfs(graph, 'C')) # {'E', 'D', 'F', 'A', 'C', 'B'}

# print ("Hi!")