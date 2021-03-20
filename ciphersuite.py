# Source 1: https://docs.python.org/3/library/ssl.html

import socket
import ssl

target_url = 'google.com'

import subprocess
def out(command):
    output = subprocess.check_output(command, shell=True)
    return output

def scan_url(url):
    out("./cipherscan/cipherscan -j " + url + " > " + url)

def main():
    scan_url(target_url)

if __name__ == "__main__":
    main()

