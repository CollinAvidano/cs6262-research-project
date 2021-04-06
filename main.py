import re
import os
import configparser
import json
import logging
import dns_failover
import ports_os
import traceroute
import certs
import ciphersuite
import forms
import template_checker
import mysql.connector

def scan_url(url):
    results = {}
    results['dns_result'] = dns_failover.check_dns(url).__dict__
    # results['ip_to_open_ports'] = {}
    # results['ip_to_traceroutes'] = {}
    #print("\n\n IPV4 START")
    # for ip in results['dns_result']['ipv4']:
    #     results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, False).__dict__
    #     results['ip_to_traceroutes'][ip] = traceroute.traceroute(ip, False)
    # print("\n\n IPV6 START")
    # for ip in results['dns_result']['ipv6']:
    #     results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, True).__dict__
        # results['ip_to_traceroutes'][ip] = traceroute.traceroute(ip, True)
    # results['cert_result'] = certs.check_cert(url).__dict__
    # results['form_result'] = forms.check_forms(url)
    # results['templating_result'] = template_checker.check_templating(url)
    # results['ciphers_result'] = ciphersuite.check_ciphers(url)

    return results
# I just dont care...

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
    )

    cursor = db.cursor() #object to execute SQL statements and interact with SQL server

    cursor.execute("DROP DATABASE IF EXISTS website_vulnerabilities")
    cursor.execute("CREATE DATABASE website_vulnerabilities")

    cursor.execute("CREATE TABLE website_vulnerabilities.website (url VARCHAR(55) PRIMARY KEY)")
    cursor.execute("CREATE TABLE website_vulnerabilities.sub_domain (parent_url VARCHAR(50), child_url VARCHAR(50) PRIMARY KEY, FOREIGN KEY(parent_url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.ip_address (url VARCHAR(50), ip_address VARCHAR(50) PRIMARY KEY, ip_version VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.cert (url VARCHAR(50), certificate VARCHAR(50), country VARCHAR(50), issued_to VARCHAR(50), organization VARCHAR(50), province VARCHAR(50), issued_by VARCHAR(50), PRIMARY KEY(url, certificate), FOREIGN KEY(url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.cipher (url VARCHAR(55), cipher VARCHAR(55), PRIMARY KEY(url, cipher), FOREIGN KEY(url) REFERENCES website(url) )")
    cursor.execute("CREATE TABLE website_vulnerabilities.port (ip_addr VARCHAR(55), port_number VARCHAR(10), protocol VARCHAR(50), PRIMARY KEY (ip_addr, port_number), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
    cursor.execute("CREATE TABLE website_vulnerabilities.os (ip_addr VARCHAR(50), version VARCHAR(50), PRIMARY KEY (ip_addr, version), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
    cursor.execute("CREATE TABLE website_vulnerabilities.traceroute (ip_addr VARCHAR(50), sender_ttl VARCHAR(50), receiver_source VARCHAR(50), sender_time VARCHAR(50), receiver_time VARCHAR(50), PRIMARY KEY (ip_addr, sender_ttl), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")

    websites = ['google.com', 'urbanasacs.com']
    
    for website in websites: 
        print(scan_url(website))
        #print(website, results['dns_result'])
        #print(results['ip_to_open_ports'])

        sql = "INSERT INTO website_vulnerabilities.website (url) VALUES (%s)"
        val = (website,)
        cursor.execute(sql, val)

        sql = "INSERT INTO website_vulnerabilities.sub_domain (parent_url, child_url) VALUES (%s,%s)"
        val = (website, website,)
        cursor.execute(sql, val)

        # for ip in results['dns_result']['ipv4']:
        #     sql = "INSERT INTO website_vulnerabilities.ip_address (url, ip_address, ip_version) VALUES (%s,%s,%s)"
        #     val = (website, ip, 'ipv4',)
        #     cursor.execute(sql, val)
        # for ip in results['dns_result']['ipv6']:
        #     sql = "INSERT INTO website_vulnerabilities.ip_address (url, ip_address, ip_version) VALUES (%s,%s,%s)"
        #     val = (website, ip, 'ipv6',)
        #     cursor.execute(sql, val)

        db.commit()


