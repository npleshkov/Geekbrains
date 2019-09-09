import yaml
from pprint import pprint

with open('write.yaml','w') as file:
    with open('source.yaml') as file_r:
        reader = yaml.safe_load(file_r)
        yaml.safe_dump(reader, file)
