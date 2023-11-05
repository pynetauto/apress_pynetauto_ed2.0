#!/usr/bin/env python3
import time
import socket
import difflib
from getpass import getpass
from netmiko import ConnectHandler

def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    username= get_input("Enter Network Admin ID     : ")
    password = None
    while not password:
        password = getpass("Enter Network Admin PWD    : ")
        password_verify = getpass("Confirm Network Admin PWD   : ")
        if password != password_verify:
            print("Passwords do not match. Please try again.")
            password = None
    return username, password

def get_device_ip():
    first_ip = get_input("Enter primary device IP      : ")
    while not first_ip:
        first_ip = get_input("* Enter primary device IP     : ")
    second_ip = get_input("Enter secondary device IP    : ")
    while not second_ip:
        second_ip = get_input("* Enter secondary device IP : ")
    return first_ip, second_ip

print("-"*79)
username, password = get_credentials()
first_ip, second_ip = get_device_ip()
print("-"*79)

device1 = {
    'device_type': 'cisco_ios',
    'ip': first_ip,
    'username': username,
    'password': password,
}

device2 = {
    'device_type': 'cisco_ios',
    'ip': second_ip,
    'username': username,
    'password': password,
}

devices = [device1, device2]

for device in devices:
    ip = device.get("ip", "")
    for port in range (22, 23):
        dest = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                connection = sock.connect(dest)
                print(f"on {ip}, port {port} is open!")
        except:
            print(f"On {ip}, port {port} is closed. Check the connectivity to {ip} again.")
            exit()

response = input(f"Make a comparison of {first_ip} and {second_ip} now? [Yes/No]")
response = response.lower()

if response == 'yes':
    print(f"* Now making a comparison : {first_ip} vs {second_ip}")
    for device in devices:
        ip = device.get("ip", "")
        try:
            net_connect = ConnectHandler(**device)
            net_connect.send_command("terminal length 0\n")
            output = net_connect.send_command("show running-config\n")
            show_run_file = open(f"{ip}_show_run.txt", "w+")
            show_run_file.write(output)
            show_run_file.close()
            time.sleep(1)
            net_connect.disconnect()
        except KeyboardInterrupt:
            print("-"*79)
else:
    print("You have selected No. Exiting the application.")
    exit()

device1_run = f"./{first_ip}_show_run.txt"
device2_run = f"./{second_ip}_show_run.txt"
device1_run_lines = open(device1_run).readlines()
time.sleep(1)
device2_run_lines = open(device2_run).readlines()
time.sleep(1)

difference = difflib.HtmlDiff(wrapcolumn=60).make_file(device1_run_lines, device2_run_lines, device1_run, device2_run)
difference_report = open(first_ip + "_vs_" + second_ip + "_compared.html", "w")
difference_report.write(difference)
difference_report.close()
print("** Device configuration comparison completed. Please Check the html file to check the differences.")
print("-"*79)
time.sleep(1)
