import concurrent.futures
import time
import main
import mysql

import csv
from collections import defaultdict

def method(url):
    print("thread-" + str(url))
    time.sleep(2)
    return url + 4

def commit(future):
    if (future is None or future.result() is None):
        print("None in future or results ({future} or {future.result()})")
        return
    website = future.result()[0]
    results = future.result()[1]
    try:
        sql = "INSERT INTO website_vulnerabilities.website (url) VALUES (%s)"
        val = (website,)
        cursor.execute(sql, val)

        sql = "INSERT INTO website_vulnerabilities.sub_domain (parent_url, child_url) VALUES (%s,%s)"
        val = (website, website,)
        cursor.execute(sql, val)

        for ip in results['dns_result']['ipv4']:
            sql = "INSERT INTO website_vulnerabilities.ip_address (url, ip_address, ip_version) VALUES (%s,%s,%s)"
            val = (website, ip, 'ipv4',)
            cursor.execute(sql, val)

            for tcp_port in results['ip_to_open_ports'][ip]['active_ports_tcp']:
                sql = "INSERT INTO website_vulnerabilities.port (ip_addr, port_number, protocol) VALUES (%s,%s,%s)"
                val = (ip, tcp_port, 'tcp',)
                cursor.execute(sql, val)
            for udp_port in results['ip_to_open_ports'][ip]['active_ports_udp']:
                sql = "INSERT INTO website_vulnerabilities.port (ip_addr, port_number, protocol) VALUES (%s,%s,%s)"
                val = (ip, udp_port, 'udp',)
                cursor.execute(sql, val)
            for trace in results['ip_to_traceroutes'][ip]:
                sql = "INSERT INTO website_vulnerabilities.traceroute (ip_addr, sender_ttl, receiver_source, sender_time, receiver_time) VALUES (%s,%s,%s,%s,%s)"
                val = (ip, trace['ttl'], trace['src'], trace['time_sent'], trace['time_received'],)
                cursor.execute(sql, val)

        for ip in results['dns_result']['ipv6']:
            sql = "INSERT INTO website_vulnerabilities.ip_address (url, ip_address, ip_version) VALUES (%s,%s,%s)"
            val = (website, ip, 'ipv6',)
            cursor.execute(sql, val)

        sql = "INSERT INTO website_vulnerabilities.cert (url, issued_to, issued_by, organization, country, location) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (website,results['cert_result']['issued_to'], results['cert_result']['issued_by'],results['cert_result']['organization'],results['cert_result']['country'],results['cert_result']['location'],)
        cursor.execute(sql, val)

        for cipher in results['ciphers_result']['ciphersuite']:
            sql = "INSERT INTO website_vulnerabilities.cipher (url, cipher) VALUES (%s,%s)"
            val = (website, cipher['cipher'],)
            cursor.execute(sql, val)

        forms_list = results['form_result'][1:]
        for form in forms_list:
            sql = "INSERT INTO website_vulnerabilities.forms (url, class, type) VALUES (%s,%s,%s)"
            val = (website, form[0], form[1],)
            cursor.execute(sql, val)

        sql = "INSERT INTO website_vulnerabilities.template (url, temp) VALUES (%s,%s)"
        val = (website, results['templating_result'],)
        cursor.execute(sql, val)

        db.commit()
    except:
        #print(f"ret is None:{ret is None}")
        print(f"On URL:{website}")
        print(f"ret[1].result() is None:{results is None}")
        print(f"ret[1].result() is None:{results}")
        # raise
    print("Commited {website}")

## Import CSV of sites
columns = defaultdict(list) # each value in each column is appended to a list

with open('rando_site.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format

    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

url_list = columns['Sites'] ##List

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server

cursor.execute("DROP DATABASE IF EXISTS website_vulnerabilities")
cursor.execute("CREATE DATABASE website_vulnerabilities")

cursor.execute("CREATE TABLE website_vulnerabilities.website (url VARCHAR(50) PRIMARY KEY)")
cursor.execute("CREATE TABLE website_vulnerabilities.sub_domain (parent_url VARCHAR(50), child_url VARCHAR(50) PRIMARY KEY, FOREIGN KEY(parent_url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.ip_address (url VARCHAR(50), ip_address VARCHAR(50) PRIMARY KEY, ip_version VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.cert (url VARCHAR(50), issued_to VARCHAR(50), issued_by VARCHAR(50), organization VARCHAR(50), country VARCHAR(50), location VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.cipher (url VARCHAR(50), cipher VARCHAR(50), PRIMARY KEY(url, cipher), FOREIGN KEY(url) REFERENCES website(url) )")
cursor.execute("CREATE TABLE website_vulnerabilities.port (ip_addr VARCHAR(50), port_number VARCHAR(10), protocol VARCHAR(50), PRIMARY KEY (ip_addr, port_number), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
cursor.execute("CREATE TABLE website_vulnerabilities.os (ip_addr VARCHAR(50), version VARCHAR(50), PRIMARY KEY (ip_addr, version), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
cursor.execute("CREATE TABLE website_vulnerabilities.traceroute (ip_addr VARCHAR(50), sender_ttl VARCHAR(50), receiver_source VARCHAR(50), sender_time VARCHAR(50), receiver_time VARCHAR(50), PRIMARY KEY (ip_addr, sender_ttl), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
cursor.execute("CREATE TABLE website_vulnerabilities.forms (url VARCHAR(50), class VARCHAR(500), type VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.template (url VARCHAR(50) PRIMARY KEY, temp VARCHAR(500), FOREIGN KEY(url) REFERENCES website(url))")

start_index = 0
number = 16

with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor: ##Limit max number of threads to 8
    for i in range(start_index, start_index + number):
        future = executor.submit(main.scan_url, url_list[i], cursor, i)
        future.add_done_callback(commit)

    #for i in range(start_index, start_index + number):
        #loop.run_in_executor(executor, main.scan_url, url_list[i], cursor, i)