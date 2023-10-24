# Filename: ch10_telnet1.py
import getpass
import telnetlib
HOST = "7.7.7.2"
user = input("Enter your telnet username: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"configure terminal\n")
tn.write(b"interface loopback 0\n")
tn.write(b"ip address 1.1.1.1 255.255.255.255\n")
tn.write(b"interface f0/1\n")
tn.write(b"ip address 20.20.20.1 255.255.255.0\n")
tn.write(b"no shut\n")
tn.write(b"end\n")
tn.write(b"show ip interface brief\n")
tn.write(b"write memory\n")
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))