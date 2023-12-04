import os
import time
from ping_6_module import check_port  # importing check_port tool from ping_6_module.py

t = time.mktime(time.localtime())
ip_add_file = './ip_addresses.txt'
f1 = open('reachable_ips_ssh.txt',  'w+')
f2 = open('reachable_ips_telnet.txt', 'w+')
f3 = open('unreachable_ips.txt', 'w+')

with open(ip_add_file, 'r') as ip_addresses:
    for ip in ip_addresses:
        ip = ip.strip()
        resp = os.system('ping -c 3 ' + ip)
        if resp == 0:
            check_port(ip, f1, f2, f3)  # parsing arguments ip, f1, f2, f3
        else:
            print(f"{ip} unreachable")
            f3.write(f"{ip} unreachable\n")

f1.close()
f2.close()
f3.close()

tt = time.mktime(time.localtime()) - t
print("Total wait time : {0} seconds".format(tt))
