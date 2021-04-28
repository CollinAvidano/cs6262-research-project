import mysql.connector
import re

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server
cursor.execute("USE website_vulnerabilities")

counts = dict()

cursor.execute('select * from template where temp like "%Wordpress%";')
total = 0
for result in cursor:
    result = result[1]
    match = re.match(r".*WordPress (\d\.\d)(\.\d)?", result)
    if match is not None:
        result = match.group(0)
        if result not in counts:
            counts[result] = 0
        counts[result] += 1
        total += 1

for key in counts.keys():
    print(f"{key}: {counts[key]}")

print(total)
