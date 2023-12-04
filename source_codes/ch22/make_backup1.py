import time
from netmiko import ConnectHandler

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

devices_list = [device1, device2]

for device in devices_list:
    ip = str(device['host'])
    f1 = open(ip + '_show_run_1.txt', 'w+')
    net_connect = ConnectHandler(**device)
    net_connect.send_command("terminal length 0")
    showrun = net_connect.send_command("show running-config")
    f1.write(showrun)
    time.sleep(1)
    f1.close()

    f2 = open(ip + '_show_ip_route_1.txt', 'w')
    showiproute = net_connect.send_command("show ip route")
    f2.write(showiproute)
    time.sleep(1)
    f2.close()

    f3 = open(ip + '_show_ip_int_bri_1.txt', 'w')
    showiproute = net_connect.send_command("show ip interface brief")
    f3.write(showiproute)
    time.sleep(1)
    f3.close()

print("All tasks completed successfully")
