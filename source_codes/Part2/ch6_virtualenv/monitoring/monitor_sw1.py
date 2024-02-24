import socket
import time
from datetime import datetime
from send_email import send_email

IP_ADDRESS = "192.168.127.101"
PORT = 22
TIMEOUT = 3
MAX_CHECKS = 10

def check_sw1():
    checks_passed = 0
    while checks_passed < MAX_CHECKS:
        with open('./monitoring_logs.txt', 'a') as f:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(TIMEOUT)
                    s.connect((IP_ADDRESS, PORT))
                    checks_passed = 0  # Reset checks count on success
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Port {PORT} is open\n")
                    print(f"Port {PORT} is open")
                    time.sleep(3)
            except socket.error:
                checks_passed += 1
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Port {PORT} is closed\n")
                print(f"Port {PORT} is closed")
                time.sleep(3)
                if checks_passed == MAX_CHECKS:
                    print("Sending failed email notification")
                    send_email()
                    break

if __name__ == "__main__":
    while True:
        check_sw1()  # Continuous rerun of the check_sw1 function
