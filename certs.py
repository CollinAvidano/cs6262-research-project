# Source 1: https://stackoverflow.com/questions/45478536/python-getting-common-name-from-url-using-ssl-getpeercert
# Source 2: https://www.programcreek.com/python/example/62606/ssl.get_server_certificate
# Source 3: https://docs.python.org/3/library/ssl.html

import socket
import ssl

class cert_results:
    organization=''
    issued_to=''
    issued_by=''
    country=''
    location=''

    def __init__(self, organization='', issued_to='', issued_by='', country='', location=''):
        self.organization=organization
        self.issued_to=issued_to
        self.issued_by=issued_by
        self.country=country
        self.location=location

def check_cert(target_url):
  
    try:
        cert = ssl.get_server_certificate((target_url, 443))
        ctx = ssl.create_default_context()
        socks = socket.socket()
        sock = ctx.wrap_socket(socks, server_hostname=target_url)
        sock.connect((target_url, 443))
        certs = sock.getpeercert()

        subject = dict(x[0] for x in certs['subject'])

        country = subject['countryName'] if 'countryName' in subject else None
        issued_to = subject['commonName'] if 'commonName' in subject else None
        organization = subject['organizationName'] if 'organizationName' in subject else None
        location = subject['stateOrProvinceName'] if 'stateOrProvinceName' in subject else None

        issuer = dict(x[0] for x in certs['issuer'])
        issued_by = issuer['commonName']

        return cert_results(organization, issued_to, issued_by, country, location)
    except ssl.SSLError as err:
        return None

if __name__ == "__main__":
    print(check_cert("google.com"))