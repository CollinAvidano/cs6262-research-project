from scapy.layers.inet import traceroute

def check_traceroute(ip):
    response, unanswered = traceroute(ip, maxttl=30)
    result = []
    for send, receive in response:
        result.append(dict({'ttl': send.ttl, 'src': receive.src, 'time_sent': send.sent_time, 'time_received': receive.time}))
    return result

if __name__ == "__main__":
    print(check_traceroute('google.com'))
