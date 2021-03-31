# Source 1: https://docs.python.org/3/library/ssl.html

import socket
import ssl
import json
import subprocess

def out(command):
    output = subprocess.check_output(command, shell=True)
    return output

def scan_url(url):
    serialized_json = out("./cipherscan/cipherscan -j " + url)
    json_dict = json.loads(serialized_json)
    return json_dict

# target_url = 'google.com'

# def main():
#     scan_url(target_url)

# if __name__ == "__main__":
#     main()
