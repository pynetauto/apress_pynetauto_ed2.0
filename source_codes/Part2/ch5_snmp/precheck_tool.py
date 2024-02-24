#!/usr/bin/python3
import os

def icmp_pinger(ip):
    # Use subprocess module for more flexibility
    try:
        rep = os.system(f'ping -c 3 {ip}')
        if rep == 0:
            print(f"{ip} is reachable.")  # Print IP is reachable if the device is on the network
        else:
            print(f"{ip} is either offline or ICMP is filtered. Exiting.")
            exit()  # Exit application if any IP address is unreachable.
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 80)

# Example usage:
# Replace '192.168.1.1' with the desired IP address
# icmp_pinger('192.168.1.1')

