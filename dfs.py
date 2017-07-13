#!/usr/bin/python

import os


# if is directory, should have children

# ideally...
treeData = [
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
                "name": "thirdfile.txt",
                "parent": "third",
            ]
          },
          {
            "name": "fourth",
            "parent": "second",
            "children" : [
                "name": "fourthfile.txt",
                "parent": "fourth",
            ]
          }
        ]
      },

      {
        "name": "second2",
        "parent": "top",
        "children" : [
            "name" : "second2file.txt",
            "parent": "second2".
        ]
      },
    ]
  }
] # close treeData

graph = {
    
}



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