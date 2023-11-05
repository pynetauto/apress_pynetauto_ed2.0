#!/usr/bin/env python3
import re
from netmiko import ConnectHandler
from getpass import getpass
import time
import socket

def get_credentials():
    global username
    global password
    username = input("Enter your username : ")
    password = None
    while not password:
        password = getpass()
        password_verify = getpass("Retype your password : ")
        if password != password_verify:
            print("Passwords do not match. Please try again.")
            password = None
    return username, password

get_credentials()

device1 = {'device_type': 'cisco_ios', 'ip': '192.168.127.3', 'username': username, 'password': password}
device2 = {'device_type': 'cisco_ios', 'ip': '192.168.127.4', 'username': username, 'password': password}
device3 = {'device_type': 'cisco_ios', 'ip': '192.168.127.101', 'username': username, 'password': password}
device4 = {'device_type': 'cisco_ios', 'ip': '192.168.127.102', 'username': username, 'password': password}
device5 = {'device_type': 'cisco_ios', 'ip': '192.168.127.133', 'username': username, 'password': password}

devices = [device1, device2, device3, device4, device5]

for device in devices:
    ip = device.get("ip", "")
    for port in range(23, 24):
        dest = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                connection = sock.connect(dest)
                print(f"On {ip}, port {port} is open!")
                net_connect = ConnectHandler(**device)
                show_clock = net_connect.send_command("show clock\n")
                print(show_clock)
                config_commands = ['line vty 0 15', 'transport input ssh']
                net_connect.send_config_set(config_commands)
                output = net_connect.send_command("show run | b line vty")
                print()
                print('-' * 79)
                print(output)
                print('-' * 79)
                print()
                net_connect.disconnect()
        except:
            print(f"On {ip}, port {port} is closed.")
