# ch11_r1_cf1.py
# This script runs show commands and prints output to your screen.
import telnetlib

host, port, username, password = "192.168.127.134", 23, "jdoe", "Lion2Roar!"

tn = telnetlib.Telnet(host, port)

tn.read_until(b"Username: ")
tn.write(username.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

commands = [
    "show file systems",
    "show flash:",
    'terminal length 0',
    "show version"
]

output = ""
for command in commands:
    tn.write(command.encode('utf-8') + b"\n")
    tn.write(b"\n")
    output += tn.read_until(b"0x2102", timeout=3).decode('utf-8')

print(output)

tn.close()
