import getpass
import telnetlib

HOST = "192.168.127.133"
user = input("Enter your username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"show ip ospf neighbor\n")
#output1 = tn.read_until(b"", timeout=10).decode('utf-8')
#print(output1)

tn.write(b"ping 2.2.2.2\n")
output2 = tn.read_until(b"ms", timeout=10).decode('utf-8')
print(output2)

tn.write(b"ping 4.4.4.4\n")
output3 = tn.read_until(b"ms", timeout=10).decode('utf-8')
print(output3)

tn.write(b"exit\n")

tn.close()
