import socket

def check_port(ip, f1, f2, f3):
    for port in range(22, 23):
        destination = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                connection = s.connect(destination)
                print(f"{ip} {port} open")
                f1.write(f"{ip}\n")
        except:
            print(f"{ip} {port} closed")
            f3.write(f"{ip} {port} closed\n")

    for port in range(23, 24):
        destination = (ip, port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                connection = s.connect(destination)
                print(f"{ip} {port} open")
                f2.write(f"{ip}\n")
        except:
            print(f"{ip} {port} closed")
            f3.write(f"{ip} {port} closed\n")
