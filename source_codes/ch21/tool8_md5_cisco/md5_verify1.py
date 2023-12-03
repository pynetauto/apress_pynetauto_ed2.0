from netmiko import ConnectHandler, SCPConn
import threading
import time
import re
from netmiko import NetMikoTimeoutException

# Verification parameters
d_newios = "c8000v-Dev-File-Only.bin" # From development 7
newiosmd5 = "563797308a3036337c3dee9b4ab54649" # From development 7

# Device configurations
device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2  # Run netmiko commands twice slower
    "read_timeout_override": 90,
}
device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
    "read_timeout_override": 90,
}
devices_list = [device1, device2]

def upload_file(device):
    ip = str(device['host'])
    try:
        net_connect = ConnectHandler(**device)
        net_connect.send_command("terminal length 0")
        locate_newios = net_connect.send_command(f"show flash: | in {d_newios}")

        # If new IOS is found on the router's flash, run this script
        if d_newios in locate_newios:
            # Cisco IOS/IOS XE verify command, run and assign variable result to the output
            result = net_connect.send_command(f"verify /md5 flash:{d_newios} {newiosmd5}", read_timeout=120) 
            print(f"Connecting to {ip}...") # Print the connected device host IP
            print(result)
            net_connect.disconnect()
            p1 = re.compile(r'Verified') # Regular Expression (re) compiler for word 'Verified'
            p2 = re.compile(r'[a-fA-F0-9]{31}[a-fA-F0-9]') # re compiler for MD5 value
            verified = p1.findall(result) # If 'Verified' was found in result, run this part of the script
            newiosmd5flash = p2.findall(result)

            if verified:
                result = True
                print(f"Connecting to {ip}...") # Print the connected device host IP
                print("MD5 values MATCH! Continue")
                print("MD5 of new IOS on Server : ", newiosmd5)
                print("MD5 of new IOS on flash  : ", newiosmd5flash[0])
                print("-" * 80)
            else: # If 'Verified' was not found in result, print and exit the application
                result = False
                print(f"Connecting to {ip}...") # Print the connected device host IP
                print("MD5 values DO NOT MATCH! Exiting.")
                print("-" * 80)
                exit()
        else: # If no new IOS file was found on the router's flash:/. Print the statement
            print(f"Connecting to {ip}...") # Print the connected device host IP
            print("No new IOS found on router's flash. Continue to next device...")
            print("-" * 80)
    except NetMikoTimeoutException as e: # Handle Timeout error due to network issue
        print(f'Timeout error to : {ip}')
        print("-" * 80)
    except Exception as unknown_error: # Handle other errors as exception
        print(f'Unknown error occurred: {unknown_error}')
        print("-" * 80)

def perform_verification_and_upload(devices):
    threads = []
    for device in devices:
        thread = threading.Thread(target=upload_file, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All file uploads and verifications completed.")

perform_verification_and_upload(devices_list)
