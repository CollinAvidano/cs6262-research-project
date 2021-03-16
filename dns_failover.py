import dns
import dns.resolver
import sys

websites = ['amazon.com', 'gatech.edu']

for website in websites:
	print(website)

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

	for ipType in listOfIPv4, listOfIPv6:
		for ip in ipType:
			print('IP address: ', ip.to_text())

	print('Failover (number of servers):', len(listOfIPv4) + len(listOfIPv6))

