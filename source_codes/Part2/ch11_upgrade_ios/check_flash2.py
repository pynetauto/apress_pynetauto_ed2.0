import time
from netmiko import ConnectHandler
import re

devices_list = [
    {
        'device_type': 'cisco_xe',
        'host': '192.168.127.111',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123'
    },
    {
        'device_type': 'cisco_xe',
        'host': '192.168.127.222',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123'
    }
]

for device in devices_list:
    net_connect = ConnectHandler(**device)
    net_connect.send_command("terminal length 0")
    showdir = net_connect.send_command("dir")
    print("-" * 80)
    time.sleep(2)
    p1 = re.compile("\d+(?=\sbytes\sfree\))")
    m1 = p1.findall(showdir)
    flashfree = (int(m1[0]) / 1000000)
    print(flashfree)
