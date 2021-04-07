import dns
import dns.resolver
import sys

# websites = ['amazon.com', 'gatech.edu']

class dns_results:
    ipv4=[]
    ipv6=[]
    failover=0

    def __init__(self, ipv4=[], ipv6=[], failover=0):
        self.ipv4=ipv4
        self.ipv6=ipv6
        self.failover=failover

def check_dns(url):
    # IPv4 dns addresses
    listOfIPv4=[]
    try:
        listOfIPv4 = dns.resolver.resolve(url, 'A')
    except dns.resolver.NoAnswer:
        listOfIPv4 = []
    except dns.resolver.NXDOMAIN:
        print('domain does not exist')
        sys.exit(1)

    # IPv6 dns addreses
    listOfIPv6=[]
    try:
        listOfIPv6 = dns.resolver.resolve(url, 'AAAA')
    except dns.resolver.NoAnswer:
        listOfIPv6 = []
    except dns.resolver.NXDOMAIN:
        print('domain does not exist')
        sys.exit(1)

    results = dns_results([], [], failover=len(listOfIPv4) + len(listOfIPv6))
    for ip in listOfIPv4:
        results.ipv4.append(ip.to_text())
    for ip in listOfIPv6:
        results.ipv6.append(ip.to_text())

    return results
    # print('Failover (number of servers):', len(listOfIPv4) + len(listOfIPv6))

if __name__ == "__main__":
    print(check_dns('amazon.com').__dict__)
