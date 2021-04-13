## I??? don't know anything about efficiency lol but this works
import csv
from collections import defaultdict
import random

sites_wanted = int(input("Enter file #:"))

columns = defaultdict(list) # each value in each column is appended to a list
count = 0

with open('top-1m.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format

    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

list_of_sites = columns['Sites'] ##List

random_site = random.sample(list_of_sites, sites_wanted)

fields = ['', 'Sites']

filename = "rando_site.csv"

rows = []

while count < sites_wanted:
	count += 1
	rows.append([count, random_site[count - 1]])

with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)

