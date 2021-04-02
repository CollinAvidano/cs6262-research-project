import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server

cursor.execute("DROP DATABASE IF EXISTS website_vulnerabilities")
cursor.execute("CREATE DATABASE website_vulnerabilities")

cursor.execute("CREATE TABLE website_vulnerabilities.website (url VARCHAR(55) PRIMARY KEY, date_accessed DATE NOT NULL)")
cursor.execute("CREATE TABLE website_vulnerabilities.sub_domain (parent_url VARCHAR(50), child_url VARCHAR(50) PRIMARY KEY, FOREIGN KEY(parent_url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.ip_address (url VARCHAR(50), ip_address VARCHAR(50) PRIMARY KEY, ip_version VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.cert (url VARCHAR(50), certificate VARCHAR(50), country VARCHAR(50), issued_to VARCHAR(50), organization VARCHAR(50), province VARCHAR(50), issued_by VARCHAR(50), PRIMARY KEY(url, certificate), FOREIGN KEY(url) REFERENCES website(url))")
cursor.execute("CREATE TABLE website_vulnerabilities.cipher (url VARCHAR(55), cipher VARCHAR(55), PRIMARY KEY(url, cipher), FOREIGN KEY(url) REFERENCES website(url) )")
cursor.execute("CREATE TABLE website_vulnerabilities.port (ip_addr VARCHAR(55), port_number VARCHAR(10), protocol VARCHAR(50), PRIMARY KEY (ip_addr, port_number), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
cursor.execute("CREATE TABLE website_vulnerabilities.os (ip_addr VARCHAR(50), version VARCHAR(50), PRIMARY KEY (ip_addr, version), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
cursor.execute("CREATE TABLE website_vulnerabilities.traceroute (ip_addr VARCHAR(50), sender_ttl VARCHAR(50), receiver_source VARCHAR(50), sender_time VARCHAR(50), receiver_time VARCHAR(50), PRIMARY KEY (ip_addr, sender_ttl), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")







