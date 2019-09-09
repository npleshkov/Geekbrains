import csv

with open('write.csv', 'w') as file:
    writer = csv.writer(file)
    with open('source.csv') as file_r:
        reader = csv.reader(file_r)
        for row in reader:
            writer.writerow(row)
            print(row)
