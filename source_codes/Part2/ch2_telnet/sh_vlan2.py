import getpass
import telnetlib

user = input("Enter your username: ")
password = getpass.getpass()

hosts = ["192.168.127.102", "192.168.127.101"]

for host in hosts:
    tn = telnetlib.Telnet(host)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")

    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"terminal length 0\n")
    tn.write(b"show vlan\n")
    tn.write(b"exit\n")
    output = tn.read_all().decode('ascii')
    print(f"Output for {host}:\n{output}")
