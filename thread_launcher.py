import concurrent.futures
import time
import main

import csv
from collections import defaultdict

def method(url):
    print("thread-" + str(url))
    time.sleep(2)
    return url + 4

## Import CSV of sites
columns = defaultdict(list) # each value in each column is appended to a list

with open('rando_site.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format

    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

url_list = columns['Sites'] ##List

############### TODO #################
# read URLs in to url_list
threads = []

with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor: ##Limit max number of threads to 8
    threads = [executor.submit(main.scan_url, url) for url in url_list]

############## TODO ##################
# write to database
for ret in threads:
    print(ret.result())