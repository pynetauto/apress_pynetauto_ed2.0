#!/usr/bin/env python3.10

import getpass
import telnetlib
import time

user = input("Enter your username: ")
password = getpass.getpass()

with open("ip_addresses.txt") as file:
    for ip in file:
        print("-"*79) # seperates output and helps readability
        print(f"Saving config on : {ip}")
        HOST = ip.strip()

        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")

        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"write memory\n") # save config
        tn.write(b"exit\n")

        print(tn.read_all().decode('ascii'))
