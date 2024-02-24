# ch11_r1_cf2_save.py
# This script runs show commands, prints output and save the output to a .txt file.
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

with open("ch11_r1_cf2_saved.txt", "w") as file:
    file.write(output)

print(output)
tn.close()
