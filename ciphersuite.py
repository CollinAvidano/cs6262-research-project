# Source 1: https://docs.python.org/3/library/ssl.html

import socket
import ssl

target_url = 'google.com'

ctx = ssl.create_default_context()
socks = socket.socket()
sock = ctx.wrap_socket(socks, server_hostname=target_url)
sock.connect((target_url, 443))

cipher = sock.cipher()

if cipher != None:
	print("Cipher Name: " + str(cipher[0]))
	print("SSL Protocol Version: " + str(cipher[1]))
	print("Number of Secret Bits: " + str(cipher[2]))