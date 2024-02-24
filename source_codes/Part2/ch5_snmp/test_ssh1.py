#Test SSH Connection to a single network device, only test the SSH connection via port 22.
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
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"Error: Unable to establish SSH connection to {hostname}. Details: {str(e)}")
    finally:
        # Close the SSH connection
        ssh_client.close()

if __name__ == "__main__":
    # Get user input for SSH login details
    hostname = input("Enter the hostname or IP address: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    # Test SSH login
    test_ssh_login(hostname, username, password)
