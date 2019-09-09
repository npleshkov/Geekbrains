import json
from pprint import pprint

with open('write.json','w') as file:
   with open('source.json') as file_r:
        reader = json.load(file_r)
        json.dump(reader, file, indent=4)
   print(json.dumps(reader))