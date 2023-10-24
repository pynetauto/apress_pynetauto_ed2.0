# Filename: ch10_telnet1a.py 
import getpass
import telnetlib
HOST = "7.7.7.2" # R1’s f0/0 interface IP address
user = input("Enter your telnet username: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ") # Same as the R1’s prompt, must update this line!
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

commands = [
    b"conf t\n",
    b"int loop 0\n",
    b"ip add 1.1.1.1 255.255.255.255\n",
    b"int f0/1\n",
    b"ip add 20.20.20.1 255.255.255.0\n",
    b"no shut\n",
    b"end\n",
    b"show ip int bri\n",
    b"exit\n"
]

for command in commands:
    tn.write(command)

print(tn.read_all().decode('ascii'))