import paramiko
import time

username = 'jdoe'
password = 'cisco123'
devices = ['192.168.127.3', '192.168.127.4', '192.168.127.101', '192.168.127.102', '192.168.127.133']

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip in devices:
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print(f"Connected and configuring {ip}")
    conn = ssh_client.invoke_shell()
    conn.send("conf t\n")
    conn.send("clock timezone AEST +10\n")
    conn.send("clock summer-time AEST recurring\n")
    conn.send("exit\n")
    conn.send("clock set 15:30:00 04 Nov 2023\n")
    conn.send("write memory\n")
    conn.send("exit\n")
    time.sleep(2)
    output = conn.recv(65535)
    print(output.decode())
    print(f"Time and Time Zone configured on {ip}")

ssh_client.close()
