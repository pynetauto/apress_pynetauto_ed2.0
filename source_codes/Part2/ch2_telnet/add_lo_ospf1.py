import getpass
import telnetlib

HOST = "192.168.127.3"
user = input("Enter your username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco123\n")
tn.write(b"conf t\n")
tn.write(b"int loopback 0\n")
tn.write(b"ip add 2.2.2.2 255.255.255.255\n")
tn.write(b"int loopback 1\n")
tn.write(b"ip add 4.4.4.4 255.255.255.255\n")
tn.write(b"router ospf 1\n")
tn.write(b"network 0.0.0.0 255.255.255.255 area 0\n")

tn.write(b"end\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
