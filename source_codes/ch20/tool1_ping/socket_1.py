import socket

device_list = ['10.10.10.1', '192.168.127.111', '192.172.1.33', '192.168.127.222', '192.168.127.133']

for ip in device_list:
    print("-"*80)
    for port in range (22, 24):
        destination = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                connection = s.connect(destination)
                print(f"On {ip}, SSH port {port} is open!")
        except:
            print(f"On {ip}, SSH port {port} is closed.")
