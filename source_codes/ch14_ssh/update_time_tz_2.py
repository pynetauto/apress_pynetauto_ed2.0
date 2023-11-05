import paramiko
import time

devices = [
    {'ip_address': '192.168.127.3', 'username': 'jdoe', 'password': 'cisco123'},
    {'ip_address': '192.168.127.4', 'username': 'jdoe', 'password': 'cisco123'},
    {'ip_address': '192.168.127.101', 'username': 'jdoe', 'password': 'cisco123'},
    {'ip_address': '192.168.127.102', 'username': 'jdoe', 'password': 'cisco123'},
    {'ip_address': '192.168.127.133', 'username': 'jdoe', 'password': 'cisco123'}
]

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for device in devices:
    ssh_client.connect(hostname=device['ip_address'], username=device['username'], password=device['password'], look_for_keys=False)
    print("Connected and configuring {}".format(device['ip_address']))

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

    print("Time and Time Zone configured on {}".format(device['ip_address']))

ssh_client.close()
