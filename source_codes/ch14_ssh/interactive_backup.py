#!/usr/bin/env python3
import time
import paramiko
from datetime import datetime
from getpass import getpass

t_ref = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
device_list = ["192.168.127.3", "192.168.127.4", "192.168.127.101", "192.168.127.102", "192.168.127.133"]
start_timer = time.mktime(time.localtime())

def get_credentials():
    global username, password
    username = input("*Enter Network Admin ID : ")
    password = None
    while not password:
        password = getpass("*Enter Network Admin PWD : ")
        password_verify = getpass("**Confirm Network Admin PWD : ")
        if password != password_verify:
            print("! Network Admin Passwords do not match. Please try again.")
            password = None
    return username, password

get_credentials()

for ip in device_list:
    print(t_ref)
    print("Now logging into " + (ip))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("Successful connection to " + (ip) + "\n")
    print("Now making running-config backup of " + (ip) + "\n")
    remote_connection = ssh_client.invoke_shell()
    time.sleep(3)
    remote_connection.send("copy running-config tftp\n")
    remote_connection.send("192.168.127.10\n")
    remote_connection.send((ip) + ".bak@" + (t_ref) + "\n")
    time.sleep(3)
    print()
    time.sleep(3)
    output = remote_connection.recv(65535)
    print((output).decode('ascii'))
    print(("Successfully backed-up running-config to TFTP & Disconnecting from ") + (ip) + "\n")
    print("-" * 80)
    ssh_client.close
    time.sleep(1)
    total_time = time.mktime(time.localtime()) - start_timer
    print("Total time : ", total_time, "seconds")
