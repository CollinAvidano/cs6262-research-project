from scapy.layers.inet import traceroute

def traceroute(ip):
	response, unanswered = traceroute(ip, maxttl=30)
    result = []
    for send, receive in response:
	    result.append(dict{'ttl ': send.ttl, 'src' : receive.src, 'time_sent' : send.sent_time,'recieved_time' receive.time})
    return result
