import re
import os
import configparser
import json
import logging
import certs
import ports_os
import traceroute
import template_checker
import dns_failover
import ciphersuite

def scan_url(url):
    dns_results = dns_failover()
    ip_to_open_ports = {}
    ip_to_traceroutes = {}
    for ip in dns_results.ipv4, dns_results.ipv6:
        ip_to_open_ports[ip] = ports_os.check_ports_os(ip) # object but you can use .__dict__ if you want it as a dict

    cert_result = certs.check_cert(url)
    cert_result = certs.check_cert(url)




if __name__ == "__main__":
    scan_url()
