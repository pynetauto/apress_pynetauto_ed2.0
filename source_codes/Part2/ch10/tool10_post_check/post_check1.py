import socket
import time
from netmiko import ConnectHandler

t1 = time.mktime(time.localtime())  # Timer start to measure script running time

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}
device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}
devices_list = [device1, device2]

def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

for device in devices_list:
    ip = str(device['host'])
    port = 22
    retry = 60
    delay = 10
    t1 = time.mktime(time.localtime())
    ipup = False
    for i in range(retry):
        if isOpen(ip, port):
            ipup = True
            print(f"{ip} is online. Logging into device to perform post reload check")
            net_connect = ConnectHandler(**device)
            print(net_connect.send_command("show clock"))
            break
        else:
            print("Device is still reloading. Please wait...")
            time.sleep(delay)
    t2 = time.mktime(time.localtime()) - t1
    print("Total wait time : {0} seconds".format(t2))
