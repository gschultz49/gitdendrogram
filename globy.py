import fnmatch
import os
import json


# matches = []
# for root, dirnames, filenames in os.walk('top'):
# 	print (dirnames,filenames)
# 	# for direct in dirnames:
# 	# 	print (direct)
#     # for filename in fnmatch.filter(filenames, '*/'):
#     #     matches.append(os.path.join(root, filename))
# print (matches)



# import os.path

# for path, directories, files in os.walk('C:\\Users\\GSCHULTZ\\Desktop\\gitdendrogram\\top'):
# 	print (directories,files)
# 	if file in files:
# 		print 'found %s' % os.path.join(path, file)

ideal =[
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

with open('ideal.json', 'w') as outfile:
    # pretty output
    json.dump(ideal, outfile, indent=4, sort_keys=True, separators=(',', ': '))