import getpass
import telnetlib

host = "192.168.127.134"
port = 23
username = input("Enter your username: ")
password = getpass.getpass()

ip_addresses = [
    "7.7.7.1",
    "192.168.127.2",
    "192.168.127.10",
    "192.168.127.20",
    "192.168.127.135",
    "8.8.8.8"
]

tn = telnetlib.Telnet(host, port)

tn.read_until(b"Username: ")
tn.write(username.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

for ip in ip_addresses:
    tn.write(f"ping {ip}\n".encode('utf-8'))
    tn.write(b"\n")
    output = tn.read_until(b"ms", timeout=10).decode('utf-8')
    print(f"Ping results for {ip}:\n{output}")

tn.close()