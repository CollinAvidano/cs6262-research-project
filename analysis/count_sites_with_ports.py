import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server
cursor.execute("USE website_vulnerabilities")

cursor.execute("select * from ip_address where ip_version=\"ipv4\"")
ip_to_url = dict();
for result in cursor:
    ip_to_url[result[1]] = result[0]

cursor.execute("select ip_addr, port_number from port")
ports_to_url_count = dict()
ports_count = dict()
for result in cursor:
    if result[1] not in ports_to_url_count:
        ports_to_url_count[result[1]] = set()
        ports_count[result[1]] = 0
    ports_to_url_count[result[1]].add(ip_to_url[result[0]])
    ports_count[result[1]] += 1

list_of_tuples = []
for port in ports_count.keys():
    tuple = (port, ports_count[port])
    list_of_tuples.append(tuple)

list_of_tuples = sorted(list_of_tuples, key=lambda x: -x[1])

for i in range(0, 10): #in ports_to_url_count.keys():
    port = list_of_tuples[i][0]
    print(f"{port} is open on {len(ports_to_url_count[port])} URLs")
