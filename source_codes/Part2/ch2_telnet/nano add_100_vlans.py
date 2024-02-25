#!/usr/bin/env python3.10
import getpass
import telnetlib

HOSTS = ["192.168.127.101", "192.168.127.102"]
user = input("Enter your username: ")
password = getpass.getpass()

for HOST in HOSTS:
    print("SWITCH IP : " + HOST)
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")

    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    
    tn.write(b"conf t\n")
    for n in range(700, 800):
        tn.write(f"vlan {n}\n".encode('utf-8'))
        tn.write(f"name PYTHON_VLAN_{n}\n".encode('utf-8'))
    
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))
