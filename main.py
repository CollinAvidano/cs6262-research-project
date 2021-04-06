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

def scan_url(url):
    results = {}
    results['dns_result'] = dns_failover.check_dns(url).__dict__
    results['ip_to_open_ports'] = {}
    results['ip_to_traceroutes'] = {}
    print("\n\n IPV4 START")
    for ip in results['dns_result']['ipv4']:
        results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, False).__dict__
        results['ip_to_traceroutes'][ip] = traceroute.traceroute(ip, False)
    # print("\n\n IPV6 START")
    # for ip in results['dns_result']['ipv6']:
    #     results['ip_to_open_ports'][ip] = ports_os.check_ports_os(ip, True).__dict__
        # results['ip_to_traceroutes'][ip] = traceroute.traceroute(ip, True)
    results['cert_result'] = certs.check_cert(url).__dict__
    results['form_result'] = forms.check_forms(url)
    results['templating_result'] = template_checker.check_templating(url)
    results['ciphers_result'] = ciphersuite.check_ciphers(url)

    return results
# I just dont care...

if __name__ == "__main__":
#    print(scan_url('google.com'))
#    print(scan_url('urbanasacs.com'))
    scan_url('google.com')
    scan_url('urbanasacs.com')
