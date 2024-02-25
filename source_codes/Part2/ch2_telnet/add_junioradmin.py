#!/usr/bin/env python3.10

import getpass
import telnetlib
import time

user = input("Enter your username: ")
password = getpass.getpass()

with open("ip_addresses.txt") as file:
    for ip in file:
        print("Now configuring : " + ip)
        HOST = ip.strip()
        
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        
        time.sleep(1)
        
        tn.write(b"conf t\n")
        tn.write(b"username junioradmin privilege 3 password cisco321\n")
        tn.write(b"privilege exec all level 3 show running-config\n")
        print("Added a new privilege 3 user")
        
        tn.write(b"end\n")
        tn.write(b"exit\n")
        print(tn.read_all().decode('ascii'))
