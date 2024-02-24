#!/usr/bin/python3
import time
import paramiko
from getpass import getpass
# Custom tools
from precheck_tool import precheck_ping

def configure_snmp(ip, username, password):
    ip = ip.strip()
    eng_id = ip.replace(".", "")  # Remove dot in the IP address and use it as SNMP Engine ID
    print(f"Now logging into {ip}")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print(f"Successful connection to {ip}\n")
    print("Now completing the following tasks:\n")
    remote_connection = ssh_client.invoke_shell()
    print(f"Adding SNMP configuration to {ip}")
    remote_connection.send("show clock\n")
    remote_connection.send("configure terminal\n")  # Add SNMP configurations
    remote_connection.send(f"snmp-server engineID local {eng_id}\n")
    remote_connection.send("snmp-server group GROUP1 v3 priv\n")
    remote_connection.send("snmp-server user SNMPUser1 GROUP1 v3 auth sha AUTHPass1 priv aes 128 PRIVPass1\n")
    remote_connection.send("do write\n")
    remote_connection.send("exit\n")
    time.sleep(2)
    print()
    time.sleep(2)
    output = remote_connection.recv(65535)
    print(output.decode('ascii'))
    print(f"Successfully configured {ip} & Disconnecting.")
    print("-" * 80)
    ssh_client.close()
    time.sleep(2)

# Read IP addresses from the file
file_path = '/home/jdoe/ch15_snmp_test/ip_addresses.txt'

try:
    with open(file_path, 'r') as file:
        ip_addresses = file.read().splitlines()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()

# Perform ICMP ping precheck for each IP address
for ip in ip_addresses:
    precheck_ping(ip)

# Get login credentials
username = input("Enter username: ")
password = getpass("Enter password: ")

# Perform SNMP configuration for each IP address
for ip in ip_addresses:
    configure_snmp(ip, username, password)

print("All tasks were completed successfully. Bye!")
