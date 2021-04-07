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
import traceback

import ssl
from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL
# from http import ClientSession

def scan_url(url):
    results = {}
    try:
        raise Exception('spam', 'eggs')

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
    except:
        error = traceback.format_exc()
        if os.path.exists("alerts.ini"):
            send_alerts(url, error)
        else:
            print("Error occured with URL: " + url + "\n" +"Error was: " + "\n" + error)


        # I guess we should throw our own error here to stop the threading launcher or maybe this should actually be caught by the threading launcher but since its not yet integrated doing it here
        return None



def send_alerts(url, error):
    config = configparser.ConfigParser()
    config.read('alerts.ini')
    recipients = config['alert']['recipients'].split(',')

    notification_message = "Error occured with URL: " + url

    # E-mail subject and content:
    subject = notification_message
    content = notification_message + "\n" +"Error was: " + "\n" + error

    print(content)

    # Build the EmailMessage object
    message = EmailMessage()
    message.add_header("From", str(config['alert']['sender-email']))
    message.add_header("To", str(recipients))
    message.add_header("Subject", subject)
    message.add_header("Content-type", "text/plain", charset="utf-8")
    message.set_content(content)

    # Send the alert:
    # has to use ssl to do simple mail transfer protocol with google which yeah the idea of using stmp is insecure so why not
    context = ssl.create_default_context()
    with SMTP_SSL(host=config['alert']['server'], port=config['alert']['port'], context=context) as client:
        # client.ehlo()
        client.login(config['alert']['sender-email'], config['alert']['sender-pasword'])
        client.sendmail(config['alert']['sender-email'], recipients, message.as_string())


if __name__ == "__main__":
#    print(scan_url('google.com'))
#    print(scan_url('urbanasacs.com'))
    scan_url('google.com')
    scan_url('urbanasacs.com')
