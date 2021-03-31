import dns
import dns.resolver
import sys

# websites = ['amazon.com', 'gatech.edu']

class dns_results:
    listOfIPv4=[]
    listOfIPv6=[]
    failover=0

    def __init__(self, listOfIPv4=[], listOfIPv6=[], failover=0):
        self.listOfIPv4=listOfIPv4
        self.listOfIPv6=listOfIPv6
        self.failover=failover

def check_dns(url):
	# IPv4 dns addresses
	try:
		listOfIPv4 = dns.resolver.resolve(website, 'A')
	except dns.resolver.NoAnswer:
		listOfIPv4 = []
	except dns.resolver.NXDOMAIN:
		print('domain does not exist')
		sys.exit(1)

	# IPv6 dns addreses
	try:
		listOfIPv6 = dns.resolver.resolve(website, 'AAAA')
	except dns.resolver.NoAnswer:
		listOfIPv6 = []
	except dns.resolver.NXDOMAIN:
		print('domain does not exist')
		sys.exit(1)

    results = dns_results(failover=len(listOfIPv4) + len(listOfIPv6))
	for ip in listOfIPv4:
        results.listOfIPv4.append(ip.to_text())

    for ip in listOfIPv6:
        results.listOfIPv6.append(ip.to_text())

	# print('Failover (number of servers):', len(listOfIPv4) + len(listOfIPv6))
