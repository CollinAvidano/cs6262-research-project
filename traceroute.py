from scapy.layers.inet import traceroute
from scapy.layers.inet6 import traceroute6

def check_traceroute(ip, ipv6=False):
    response = None
    unanswered = None
    if ipv6:
        response, unanswered = traceroute6(ip, maxttl=30)
    else:
        response, unanswered = traceroute(ip, maxttl=30)
    result = []
    for send, receive in response:
        result.append(dict({'ttl': send.ttl, 'src': receive.src, 'time_sent': send.sent_time, 'time_received': receive.time}))
    return result

if __name__ == "__main__":
    print(check_traceroute("108.177.122.113", False))
    # print(check_traceroute("2607:f8b0:4002:0808:0000:0000:0000:200e", True))
    # print(check_traceroute("2607:f8b0:4002:808::200e", True))
