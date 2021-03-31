from scapy.layers.inet import traceroute

def traceroute(ip):
	response, unanswered = traceroute(ip, maxttl=30)
	for send, receive in response:
	    print(send.ttl, receive.src, send.sent_time, receive.time)
