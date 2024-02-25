#!/usr/bin/env python3
import getpass
import telnetlib
HOST = "192.168.127.101"
user = input("Enter your username: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
       tn.read_until(b"Password: ")
       tn.write(password.encode('ascii') + b"\n")
# Get into config mode
tn.write(b"conf t\n")
# Adds 5 vlans to the list with for loop
vlans = [101, 202, 303, 404, 505] # vlans to add in  a list
for i in vlans:
          command_1 = "vlan " + str(i) + "\n"
          tn.write(command_1.encode('ascii'))
          command_2 = "name PYTHON_VLAN_" + str(i) + "\n"
          tn.write(command_2.encode('ascii'))

tn.write(b"end\n")
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))
