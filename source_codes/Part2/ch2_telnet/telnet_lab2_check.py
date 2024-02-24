import telnetlib

host, port, username, password = "192.168.127.101", 23, "jdoe", "cisco123"

tn = telnetlib.Telnet(host, port)

tn.read_until(b"Username: ")
tn.write(username.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

commands = [
    "show vlan",
    "show ip interface brief",
    'terminal length 0',
    "show run"
]

output = ""
for command in commands:
    tn.write(command.encode('utf-8') + b"\n")
    tn.write(b"\n")
    output += tn.read_until(b"line con 0", timeout=7).decode('utf-8')

print(output)

tn.close()
