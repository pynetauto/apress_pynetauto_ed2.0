# Reads IPs from 'ip_addresses.txt' file and test SSN connection for multiple devices.
# Runs 'show clock' and output with the line seperators.
import paramiko
from getpass import getpass

def test_ssh_login(hostname, username, password):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        # Automatically add the server's host key (this is insecure, see comments)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the SSH server
        ssh_client.connect(hostname, username=username, password=password, timeout=5)

        print(f"SSH login to {hostname} successful.")

        # Run 'show clock' command
        stdin, stdout, stderr = ssh_client.exec_command("show clock")
        output = stdout.read().decode("utf-8")

        # Print the time and hostname
        print(f"\nTime on {hostname}:\n{output}")
        print("-"*79)
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"Error: Unable to establish SSH connection to {hostname}. Details: {str(e)}")
    finally:
        # Close the SSH connection
        ssh_client.close()

if __name__ == "__main__":
    # Read IP addresses from the file
    file_path = 'ip_addresses.txt'
    try:
        with open(file_path, 'r') as file:
            ip_addresses = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit()

    # Get user input for SSH login details
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    # Iterate over IP addresses and test SSH login
    for ip in ip_addresses:
        test_ssh_login(ip, username, password)
