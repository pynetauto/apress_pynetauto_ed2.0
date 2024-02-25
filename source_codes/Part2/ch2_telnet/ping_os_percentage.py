import os

def get_ping_success_rate(host):
    response = os.system("ping -c 4 " + host)
    return response

def calculate_success_rate(response):
    return (4 - response) / 4 * 100 

HOST = "192.168.127.102"

ping_response = get_ping_success_rate(HOST)

if ping_response > 3:
    print("Server is not responsive.")
else:
    print("Server is responsive.")

success_rate = calculate_success_rate(ping_response)
print(f"Ping success rate: {success_rate:.2f}%")  
