import socket

IP_ADDRESS = '192.168.127.101'
PORT_TO_CHECK = 22
TIMEOUT = 3

def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))
            print(f"Port {port} is open on {ip}. This device is on the network.")
    except socket.error:
        print(f"Port {port} is closed on {ip}. FAILED to reach the device. Check connectivity.")
        exit()

def check_port_22():
    check_port(IP_ADDRESS, PORT_TO_CHECK)

if __name__ == "__main__":
    check_port_22()
