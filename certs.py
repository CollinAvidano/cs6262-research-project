# Source 1: https://stackoverflow.com/questions/45478536/python-getting-common-name-from-url-using-ssl-getpeercert
# Source 2: https://www.programcreek.com/python/example/62606/ssl.get_server_certificate
# Source 3: https://docs.python.org/3/library/ssl.html

import socket
import ssl

# target_url = 'google.com'

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
    cert = ssl.get_server_certificate((target_url, 443))
    ctx = ssl.create_default_context()
    socks = socket.socket()
    sock = ctx.wrap_socket(socks, server_hostname=target_url)
    sock.connect((target_url, 443))
    certs = sock.getpeercert()
    subject = dict(x[0] for x in certs['subject'])
    country = subject['countryName']
    issued_to = subject['commonName']
    organization = subject['organizationName']
    location = subject['stateOrProvinceName']
    issuer = dict(x[0] for x in certs['issuer'])
    issued_by = issuer['commonName']
    return cert_results(organization, issued_to, issued_by, country, location)

    # print(cert)
    # print('Country: ' + country)
    # print('Issued to: ' + issued_to)
    # print('Organization: ' + organization)
    # print('Province: ' + location)
    # print('Issued by: ' + issued_by)

# Now just have to save it

if __name__ == "__main__":
    print(check_cert("google.com"))
