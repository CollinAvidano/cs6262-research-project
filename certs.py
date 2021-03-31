# Source 1: https://stackoverflow.com/questions/45478536/python-getting-common-name-from-url-using-ssl-getpeercert
# Source 2: https://www.programcreek.com/python/example/62606/ssl.get_server_certificate
# Source 3: https://docs.python.org/3/library/ssl.html

import socket
import ssl

target_url = 'expired.badssl.com'

cert = ssl.get_server_certificate((target_url, 443))
ctx = ssl.create_default_context()
socks = socket.socket()
sock = ctx.wrap_socket(socks, server_hostname=target_url)
go = True
try:
    sock.connect((target_url, 443))
except ssl.SSLError as err:
    print("Certificate is invalid (" + str(err.reason) + ")")
    go = False

if go:
    certs = sock.getpeercert()

    print(cert)

    subject = dict(x[0] for x in certs['subject'])

    to_inspect = {'countryName', 'commonName', 'organizationName', 'stateOrProvinceName'}
    other_values = dict()

    for key in to_inspect:
        if key in subject:
            print(str(key) + ": " + str(subject['countryName']))

    issuer = dict(x[0] for x in certs['issuer'])
    issued_by = issuer['commonName']

    print('Issued by: ' + issued_by)

    # Now just have to save it