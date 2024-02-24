import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = ("192.168.127.3", 80)
port_open = sock.connect_ex(dest)

if port_open == 0:
    print(port_open)
    print(f"On {dest[0]}, port {dest[1]} is open.")
else:
    print(port_open)
    print(f"On {dest[0]}, port {dest[1]} is closed.")
sock.close()
