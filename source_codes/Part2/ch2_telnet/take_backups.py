#!/usr/bin/env python3.10
import getpass
import telnetlib
from datetime import datetime

saved_time = datetime.now().strftime("%Y%m%d_%H%M%S")

user = input("Enter your username: ")
password = getpass.getpass()

file = open("ip_addresses.txt")

for ip in file:
    print("Back up running-config of " + (ip))

    HOST = ip.strip()
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")

    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(("terminal length 0\n").encode('ascii'))
    tn.write(("show clock\n").encode('ascii'))
    tn.write(("show running-config\n").encode('ascii'))
    tn.write(("exit\n").encode('ascii'))

    readoutput = tn.read_all()
    saveoutput = open(str(saved_time) + "_running_config_" + HOST, "wb")
    saveoutput.write(readoutput)
    saveoutput.close()
