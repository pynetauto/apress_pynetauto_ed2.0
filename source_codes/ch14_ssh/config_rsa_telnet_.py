import getpass
import telnetlib
import time

# Function to configure the devices
def configure_device(device_ip, commands):
    try:
        # Define login details
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Telnet connection
        tn = telnetlib.Telnet(device_ip)
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        # Entering configuration mode
        tn.write(b"enable\n")
        tn.write(b"conf t\n")
        time.sleep(1)

        # Sending configuration commands
        for command in commands:
            tn.write(command.encode('ascii') + b"\n")
            time.sleep(1)

        # Exiting configuration mode and saving the configuration
        tn.write(b"end\n")
        tn.write(b"write memory\n")
        time.sleep(1)

        # Close the connection
        tn.write(b"exit\n")
        print(f"Configuration on {device_ip} completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Commands to be configured
commands_to_configure = [
    "ip domain-name pynetauto.local",
    "crypto key generate rsa",
    "1024",
    "line vty 0 15",
    "transport input all",
    "end",
    "write memory"
]

# List of devices
devices = {
    "R1": "192.168.127.133",
    "R2": "192.168.127.3",
    "r3": "192.168.127.4",
    "SW1": "192.168.127.101",
    "sw2": "192.168.127.102"
}

# Configure each device
for device_name, device_ip in devices.items():
    print(f"Configuring {device_name}...")
    configure_device(device_ip, commands_to_configure)
