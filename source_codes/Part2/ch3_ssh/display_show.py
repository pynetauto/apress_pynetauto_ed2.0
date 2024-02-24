import paramiko
import time

username = 'jdoe'
password = 'cisco123'
devices = [
#'192.168.127.133',
'192.168.127.3',
'192.168.127.4',
#'192.168.127.101',
#'192.168.127.102'
]

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip in devices:
    ssh_client.connect(ip, 22, username=username, password=password, look_for_keys=False)
    print(f"Connected to {ip}")
    conn = ssh_client.invoke_shell()
    conn.send("show ntp associations\n")
    conn.send("show ntp status\n")
    time.sleep(2)
    output = conn.recv(65535)
    print(output.decode())
    print("-"*79)

ssh_client.close()
