import subprocess

# List of IP addresses
ip_addresses = ['192.168.127.3', '192.168.127.4', '192.168.127.101', '192.168.127.102']

# Loop through the IP addresses and run ssh-keygen command for each
for ip in ip_addresses:
    command = f"ssh-keygen -F {ip}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Print the output
    print(stdout.decode())
    if stderr:
        print(stderr.decode())
