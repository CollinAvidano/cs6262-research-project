import socket
import ssl

hostname = 'google.com'
ctx = ssl.create_default_context()
s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
s.connect((hostname, 443))
cert = s.getpeercert()
print(cert)


# SSL Certificates from above, but prettier. 
# Source: https://www.programcreek.com/python/example/62606/ssl.get_server_certificate

# def ssl_cert():
#     """Get the ssl cert of a website."""
#     print colored('Enter a URL to get its SSL cert', 'green')
#     target_url = raw_input(colored('(netpwn: ssl_cert) > ', 'red'))

#     try:
#         cert = ssl.get_server_certificate((target_url, 443))
#         ctx = ssl.create_default_context()
#         socks = socket.socket()
#         sock = ctx.wrap_socket(socks, server_hostname=target_url)
#         sock.connect((target_url, 443))
#         certs = sock.getpeercert()
#         subject = dict(x[0] for x in certs['subject'])
#         country = subject['countryName']
#         issued_to = subject['commonName']
#         organization = subject['organizationName']
#         location = subject['stateOrProvinceName']
#         issuer = dict(x[0] for x in certs['issuer'])
#         issued_by = issuer['commonName']
#         print colored(cert, 'green')
#         print colored('Country: ' + country, 'green')
#         print colored('Issued to: ' + issued_to, 'green')
#         print colored('Organization: ' + organization, 'green')
#         print colored('Province: ' + location, 'green')
#         print colored('Issued by: ' + issued_by, 'green')
#         print ' '

#     except socket.error:
#         print colored('Unknown host: ' + target_url, 'yellow')

#     except KeyError:
#         print colored('No SSL cert', 'yellow') 

# Test: getpeercent(True)
# Source: https://stackoverflow.com/questions/45478536/python-getting-common-name-from-url-using-ssl-getpeercert

# import socket
# import ssl
# import OpenSSL.crypto as crypto

# dst = ('cds.ca',443)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(dst)

# # upgrade the socket to SSL without checking the certificate
# # !!!! don't transfer any sensitive data over this socket !!!!
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# s = ctx.wrap_socket(s, server_hostname=dst[0])

# # get certificate
# cert_bin = s.getpeercert(True)
# x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert_bin)
# print("CN=" + x509.get_subject().CN)