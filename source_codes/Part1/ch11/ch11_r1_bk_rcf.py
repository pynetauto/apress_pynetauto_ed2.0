# ch11_bk_rcf.py
# Runs and saves running-config of R1
import getpass
import telnetlib

HOST = "192.168.127.134"
user = input("Enter your telnet username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"copy running-config tftp://192.168.127.10/running-config\n")
tn.write(b"\n")
tn.write(b"\n")

tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
