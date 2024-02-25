     import os

with open("ip_addresses.txt", "r") as file:
    for line in file:
        ip_address = line.split()[0]

        response = os.system(f"ping -c 4 {ip_address}")

        if response == 0:
            print(f"Ping to {ip_address} successful.")
        else:
            print(f"Ping to {ip_address} unsuccessful.")
