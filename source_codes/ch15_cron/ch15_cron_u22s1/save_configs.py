from netmiko import ConnectHandler
import time

start_time = time.time()  # Start timer

username = 'jdoe'
password = 'cisco123'
devices = [
    '192.168.127.3',
    '192.168.127.4',
    '192.168.127.101',
    '192.168.127.102',
    '192.168.127.133'
]

for ip in devices:
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password
    }

    try:
        ssh_conn = ConnectHandler(**device)
        print(f"Connected to {ip}")
        ssh_conn.send_command("write memory")
        print("saved running-config")
        time.sleep(2)
        output = ssh_conn.send_command("")
        print(output)
        print("-" * 79)
        ssh_conn.disconnect()
    except Exception as e:
        print(f"{ip} is offline")
        continue

end_time = time.time()  # End timer
execution_time = end_time - start_time  # Calculate execution time
print(f"Total execution time: {execution_time:.2f} seconds")
