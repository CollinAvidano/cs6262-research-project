import nmap
import mysql.connector
import concurrent.futures

def scan_os(idx, ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-O')
    try:
        if 'osmatch' in nm[ip]:
            os_info = nm[ip]['osmatch'][0]
            return (idx, f"{ip}: {os_info['osclass'][0]['osfamily']} {os_info['osclass'][0]['osgen']}")
    except:
        return (idx, f"{ip}: No scan")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server
cursor.execute("USE website_vulnerabilities")

cursor.execute("select * from ip_address where ip_version=\"ipv4\"")

ip_list = []
for result in cursor:
    ip_list.append(result[1])

file = open('os_analysis.txt', 'w')
idx = 0
running = []
with concurrent.futures.ThreadPoolExecutor() as executor: ##Limit max number of threads to 8
    while (idx < len(ip_list) or len(running) != 0):
        while len(running) < 8 and idx < len(ip_list):
            running.append(executor.submit(scan_os, idx, ip_list[idx]))
            idx += 1
        r = 0
        while r < len(running):
            if running[r].done():
                print(f"{running[r].result()[0]}: {running[r].result()[1]}")
                file.write(running[r].result()[1])
                file.write('\n')
                del running[r]
            else:
                r += 1
