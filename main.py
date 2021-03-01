import re
import os
import configparser
import json
import logging


def main():
    self.config.read('scanner.ini')
    connection = pymysql.connect(
        host=self.config['sql']['host'],  # Database address
        user=self.config['sql']['user'],  # database username
        password=self.config['sql']['password'],  # Database password
        db=self.config['sql']['db_name'],  # Name database
        # charset = 'utf8 -- UTF-8 Unicode'
    )

import pymysql
def store():
    sql = 'insert into sites(domain,ip,password,pid,tel) values (%s,%s,%s,%s,%s)'
    #Insert data
    data = [
        ('test1', 'male', '123456', 3, '110'),
        ('test2', None, '123456', 2, '120'),
    ]
    #Splice and execute SQL statements
    self.cursor.executemany(sql,data)
    #Related write operations to be submitted
    self.connection.commit()


import nmap
def scan(ip, port_str):
    nm = nmap.PortScanner()
    nm.scan('127.0.0.1', '22-443')
    output = nm.scaninfo()

import subprocess
def out(command):
    output = subprocess.check_output(command, shell=True)
    return output

def dig(fqdn):
    output = str(out("dig +trace " + fqdn))
    ns_records = re.findall(r"NS\\t(\S*?)\.\\n", output)
    a_records = re.findall(r"A\\t(\S*?)\\n", output)

    return ns_records, a_records

import sublist3r
def check_subdomains(fqdn)
    subdomains = sublist3r.main(fqdn, no_threads=4, savefile=None, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
    return subdomains



if __name__ == "__main__":
    main()
