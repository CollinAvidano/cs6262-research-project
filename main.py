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
    results['ip_to_open_ports'] = {}
    results['ip_to_traceroutes'] = {}
    print("\n\n IPV4 START")
    for ip in results['dns_result']['ipv4']:
        results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, False).__dict__
        results['ip_to_traceroutes'][ip] = traceroute.check_traceroute(ip, False)
    # print("\n\n IPV6 START")
    # for ip in results['dns_result']['ipv6']:
    #     results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, True).__dict__
    #     results['ip_to_traceroutes'][ip] = traceroute.traceroute(ip, True)
    results['cert_result'] = certs.check_cert(url).__dict__
    results['form_result'] = forms.check_forms(url)
    results['templating_result'] = template_checker.check_templating(url)
    results['ciphers_result'] = ciphersuite.check_ciphers(url)
    print(results)
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

    cursor.execute("CREATE TABLE website_vulnerabilities.website (url VARCHAR(50) PRIMARY KEY)")
    cursor.execute("CREATE TABLE website_vulnerabilities.sub_domain (parent_url VARCHAR(50), child_url VARCHAR(50) PRIMARY KEY, FOREIGN KEY(parent_url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.ip_address (url VARCHAR(50), ip_address VARCHAR(50) PRIMARY KEY, ip_version VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.cert (url VARCHAR(50), issued_to VARCHAR(50) PRIMARY KEY, issued_by VARCHAR(50), organization VARCHAR(50), country VARCHAR(50), location VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.cipher (url VARCHAR(50), cipher VARCHAR(50), PRIMARY KEY(url, cipher), FOREIGN KEY(url) REFERENCES website(url) )")
    cursor.execute("CREATE TABLE website_vulnerabilities.port (ip_addr VARCHAR(50), port_number VARCHAR(10), protocol VARCHAR(50), PRIMARY KEY (ip_addr, port_number), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
    cursor.execute("CREATE TABLE website_vulnerabilities.os (ip_addr VARCHAR(50), version VARCHAR(50), PRIMARY KEY (ip_addr, version), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
    cursor.execute("CREATE TABLE website_vulnerabilities.traceroute (ip_addr VARCHAR(50), sender_ttl VARCHAR(50), receiver_source VARCHAR(50), sender_time VARCHAR(50), receiver_time VARCHAR(50), PRIMARY KEY (ip_addr, sender_ttl), FOREIGN KEY(ip_addr) REFERENCES ip_address(ip_address))")
    cursor.execute("CREATE TABLE website_vulnerabilities.forms (url VARCHAR(50), class VARCHAR(50), type VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
    cursor.execute("CREATE TABLE website_vulnerabilities.template (url VARCHAR(50) PRIMARY KEY, temp VARCHAR(50), FOREIGN KEY(url) REFERENCES website(url))")
    websites = ['google.com', 'twitter.com', 'urbanasacs.com' ]
    
    for website in websites: 
        results = scan_url(website)

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
            for traceroute in results['ip_to_traceroutes'][ip]:
                sql = "INSERT INTO website_vulnerabilities.traceroute (ip_addr, sender_ttl, receiver_source, sender_time, receiver_time) VALUES (%s,%s,%s,%s,%s)"
                val = (ip, traceroute['ttl'], traceroute['src'], traceroute['time_sent'], traceroute['time_received'],)
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

        forms = results['form_result'][1:]
        for form in results['form_result'] :
            sql = "INSERT INTO website_vulnerabilities.forms (url, class, type) VALUES (%s,%s,%s)"
            val = (website, form[0], form[1],)
            cursor.execute(sql, val)

        sql = "INSERT INTO website_vulnerabilities.template (url, temp) VALUES (%s,%s)"
        val = (website, results['templating_result'],)
        cursor.execute(sql, val)

        db.commit()