#!/usr/bin/python3
import time
import paramiko
from getpass import getpass
from precheck_tool import icmp_pinger

# File paths
ip_addresses_file = "/home/jdoe/ch15_snmp_test/ip_addresses.txt"

# Read IP addresses from the file and perform pre-checks
with open(ip_addresses_file, "r") as ip_addresses:
    for ip in ip_addresses:
        ip = ip.strip()
        icmp_pinger(ip)

# Ask for username and password
username = input("Enter username: ")
password = getpass("Enter password: ")

# SNMP Configuration
def configure_snmp(ip, eng_id):
    print(f"Now logging into {ip}")

    # Establish SSH connection
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
        print(f"Successful connection to {ip}\n")
        print("Now completing the following tasks:\n")

        # Add SNMP configuration
        with ssh_client.invoke_shell() as remote_connection:
            remote_connection.send("show clock\n")
            remote_connection.send("configure terminal\n")
            remote_connection.send(f"snmp-server engineID local {eng_id}\n")
            remote_connection.send("snmp-server group GROUP1 v3 priv\n")
            remote_connection.send("snmp-server user SNMPUser1 GROUP1 v3 auth sha AUTHPass1 priv aes 128 PRIVPass1\n")
            time.sleep(2)
            remote_connection.send("do write\n")
            time.sleep(2)
            remote_connection.send("exit\n")
            time.sleep(2)
            print()
            time.sleep(2)
            output = remote_connection.recv(65535)
            print(output.decode('ascii'))
            print(f"Successfully configured {ip} & Disconnecting.")
            print("-" * 80)

# Configure SNMP on each device
with open(ip_addresses_file, "r") as ip_addresses:
    for ip in ip_addresses:
        ip = ip.strip()
        eng_id = ip.replace(".", "")  # Remove dot in IP address and use it as SNMP Engine ID
        configure_snmp(ip, eng_id)

print("All tasks were completed successfully. Bye!")
