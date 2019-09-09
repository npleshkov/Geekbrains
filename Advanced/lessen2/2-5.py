import yaml
import csv


csv_file = open('source.csv', 'r')
yaml_file = open('write-import.yaml', 'w')

# reader = csv.DictReader(csv_file)
reader = csv.reader(csv_file)
keys = next(reader)
print(reader)
with csv_file as file_r:
    for row in reader:
        yaml.dump([dict(zip(keys, row))], yaml_file)



# out = yaml.safe_dump( [ row for row in reader ] )
# print(out)
# yaml_file.write(out)
