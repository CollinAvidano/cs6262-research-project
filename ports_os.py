import nmap

# this list will be generated from the top websites (right now just an example)
# servers = ['205.251.242.103', '108.177.122.138', '128.61.5.7']
# servers = ['twitter.com']
# which ports are we trying to scan?

ports = '1-500'

class port_os_results:
    host_ip=''
    hostname=''
    protocols=[]
    active_ports_tcp=[]
    active_ports_udp=[]
    operating_system=''

    def __init__(self, host_ip='', hostname='', protocols=[], active_ports_tcp=[], active_ports_udp=[], operating_system=''):
        self.host_ip=host_ip
        self.hostname=hostname
        self.protocols=protocols
        self.active_ports_tcp=active_ports_tcp
        self.active_ports_udp=active_ports_udp
        self.operating_system=operating_system

# this will give you OS version but you have to use root privledges (not sure how to make this work)
def check_ports_os(ip, ipv6=False):
    print(ip)
    scanner = nmap.PortScanner()
    if ipv6 == True:
        scanner.scan(ip, arguments='-O -6')
    else:
        scanner.scan(ip, arguments='-O')

    print('Command Line Arguments: ', scanner.command_line())
    print('Hosts to scan: ', scanner.all_hosts())

    results = port_os_results(host_ip=ip, hostname=scanner[ip].hostname(), protocols=scanner[ip].all_protocols(), active_ports_tcp=[], active_ports_udp=[], operating_system=[])
    for protocol in scanner[ip].all_protocols():
        active_ports = scanner[ip][protocol].keys()
        for port in active_ports:
            if protocol == 'tcp':
                results.active_ports_tcp.append(port)
            elif protocol == 'udp':
                results.active_ports_udp.append(port)
            else:
                pass
    print(results.__dict__)
    #print('OS: ', scanner[ip]['osmatch'])
    return results

if __name__ == "__main__":
    # google ipv6
    check_ports_os("172.217.0.142", False)
    # check_ports_os("2607:f8b0:4002:0808:0000:0000:0000:200e", True)
    # check_ports_os("2607:f8b0:4002:808::200e", True)
