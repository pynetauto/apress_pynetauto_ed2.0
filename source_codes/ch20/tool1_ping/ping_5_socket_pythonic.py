import os
import socket
import time

t1 = time.mktime(time.localtime())

def check_port(ip):
    for port in range(22, 23):
        destination = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                connection = s.connect(destination)
                print(f"{ip} {port} opened")
                f1.write(f"{ip}\n")
        except:
            print(f"{ip} {port} closed")
            f3.write(f"{ip} {port} closed\n")
    for port in range(23, 24):
        destination = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                connection = s.connect(destination)
                print(f"{ip} {port} opened")
                f2.write(f"{ip}\n")
        except:
            print(f"{ip} {port} closed")
            f3.write(f"{ip} {port} closed\n")

ip_add_file = './ip_addresses.txt'
f1 = open('reachable_ips_ssh.txt', 'w+')
f2 = open('reachable_ips_telnet.txt', 'w+')
f3 = open('unreachable_ips.txt', 'w+')

with open(ip_add_file, 'r') as ip_addresses:
    for ip in ip_addresses:
        ip = ip.strip()
        resp = os.system('ping -c 3 ' + ip)
        if resp == 0:
            check_port(ip)
        else:
            print(f"{ip} unreachable")
            f3.write(f"{ip} unreachable\n")

f1.close()
f2.close()
f3.close()
tt = time.mktime(time.localtime()) - t1
print("Total wait time: {0} seconds".format(tt))
