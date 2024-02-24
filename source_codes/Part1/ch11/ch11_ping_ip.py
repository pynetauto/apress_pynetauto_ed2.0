# ch11_ping_ip.py
import getpass
import telnetlib

host = "192.168.127.134"
port = 23
username = "jdoe"
password = "Lion2Roar!"

tn = telnetlib.Telnet(host, port)

tn.read_until(b"Username: ")
tn.write(username.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

tn.write(b"ping 7.7.7.1\n")
tn.write(b"\n")

output = tn.read_until(b"ms", timeout=10).decode('utf-8')
print(output)

tn.close()