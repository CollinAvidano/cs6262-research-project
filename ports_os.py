import nmap

# this list will be generated from the top websites (right now just an example)
servers = ['205.251.242.103', '108.177.122.138', '128.61.5.7']
servers = ['twitter.com']
# which ports are we trying to scan? 
ports = '1-500'

for server in servers:
    scanner = nmap.PortScanner()
    #scanner.scan(server)

    # this will give you OS version but you have to use root privledges (not sure how to make this work)
    scanner.scan(server, arguments='-O')

    # print results
    for host in scanner.all_hosts():
        print('Host IP: ', host)
        print('Host Name: ', scanner[host].hostname())
        print('OS: ', scanner[host]['osmatch'])
        for protocol in scanner[host].all_protocols():
            print('Protocol : %s' % protocol)
            activePorts = scanner[host][protocol].keys()
            for port in activePorts:
                print ('port %s (%s)' % (port, scanner[host][protocol][port]['state']))


