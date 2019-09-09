import json
import csv


csv_file = open('source.csv', 'r')
json_file = open('write-import.json', 'w')

reader = csv.DictReader(csv_file)
out = json.dumps( [ row for row in reader ] )
# print(out)
json_file.write(out)


