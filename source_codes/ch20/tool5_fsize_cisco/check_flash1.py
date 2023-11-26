import time
from netmiko import ConnectHandler

# Borrowed from read_info7.py result in tool3_read_csv directory.
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
    # showflash = net_connect.send_command("show flash:") # Alternatively use 'show flash:'
    print(showdir)
    print("-" * 80)
    time.sleep(2)
