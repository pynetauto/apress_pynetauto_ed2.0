#!/usr/bin/env python3
import getpass
import telnetlib

HOST = "192.168.127.102"
user = input("Enter your username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"conf t\n")

vlans = [101, 202, 303, 404, 505]  # VLANs to add to the list
i = 0  # Initialize the index value

while i < len(vlans):  # While 'i' is less than the length of 'vlans'
    command_1 = "vlan " + str(vlans[i]) + "\n"
    tn.write(command_1.encode('ascii'))  # Send 'command_1' with ASCII encoding
    command_2 = "name PYTHON_VLAN_" + str(vlans[i]) + "\n"
    tn.write(command_2.encode('ascii'))  # Send 'command_2' with ASCII encoding
    i += 1  # Increment 'i' to move to the next VLAN in the list

tn.write(b"end\n")
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))
