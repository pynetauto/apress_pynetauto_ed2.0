import paramiko
import time

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect("192.168.127.133", 22, username="jdoe", password="cisco123", look_for_keys=False)
conn = ssh_client.invoke_shell()
conn.send("show clock\n")
time.sleep(2)
output = conn.recv(65535)
print(output.decode())
ssh_client.close()
