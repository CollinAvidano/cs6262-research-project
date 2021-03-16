from scapy.layers.inet import traceroute

websites = ['facebook.com', 'google.com']

for website in websites:
	response, unanswered = traceroute(website, maxttl=30)
	for send, receive in response:
	    print(send.ttl, receive.src, send.sent_time, receive.time)