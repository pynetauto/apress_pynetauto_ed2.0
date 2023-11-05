import socket
ip_addresses = ["192.168.127.3", "192.168.127.4", "192.168.127.101", "192.168.127.102", "192.168.127.133"]

for ip in ip_addresses:
    for port in range(22, 24):
        dest = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                connection = sock.connect(dest)
                print(f"On {ip}, port {port} is open!")
        except:
            print(f"On {ip}, port {port} is closed.")
