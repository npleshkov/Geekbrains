import json
import csv

csv_file = open('source.csv', 'r')
json_file = open('write-import.json', 'w')
reader = csv.DictReader(csv_file)

json_file.write('[''\n')
for row in reader:
    print(row)
    json.dump(row, json_file)
    json_file.write(',\n')
json_file.write(']')
