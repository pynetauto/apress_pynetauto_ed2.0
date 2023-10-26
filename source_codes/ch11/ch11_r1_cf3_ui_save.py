# ch11_r1_cf3_ui_save.py
# Runs interactively accepts show commands from user, prints output and save the output a file.
import getpass
import telnetlib

host, port, username, password = "192.168.127.134", 23, "jdoe", "Lion2Roar!"
tn = telnetlib.Telnet(host, port)
tn.read_until(b"Username: ")
tn.write(username.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

commands = []
while True:
    command = input("Enter a command to run (or press Enter to finish): ")
    if not command:
        break
    commands.append(command)

output = ""
for command in commands:
    tn.write(command.encode('utf-8') + b"\n")
    output += tn.read_until(b"0x2102", timeout=3).decode('utf-8')

with open("ch11_r1_cf3_ui_saved.txt", "w") as file:
    file.write(output)

print(output)
tn.close()
