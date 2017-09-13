import csv
import json
result={}
reader = csv.reader(open("inp.csv", "rb"))
for rows in reader:
        k = rows[0]
        v = rows[1]
        result[k] = v
print (result)
