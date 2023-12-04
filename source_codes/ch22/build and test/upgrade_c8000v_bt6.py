import socket  # For socket networking
import os  # For Python Server OS
import time  # Python time module
import pandas as pd  # Pandas for reading data into a data frame
import re  # Python regular expression module
from getpass import getpass  # For uid & password collection
import os.path  # For Python Server OS directory
import hashlib  # For MD5 checks
from netmiko import ConnectHandler, SCPConn  # netmiko SSH connection and SCP file transfer
from netmiko import NetMikoTimeoutException  # To catch netmiko timeout exceptions
import difflib  # For analyzing two files and differences

t1 = time.mktime(time.localtime()) # Timer(t1) start to measure script running time

def get_secret(p2):
    global secret # declare secret as a global variable
    resp = input("Is secret same as password? (y/n) : ")
    resp = resp.lower()
    if resp == "yes" or resp == "y":
        secret = pwd
    elif resp == "no" or resp == "n":
        secret = None
        while not secret:
            secret = getpass("Enter the secret : ")
            while not p2.match(secret):
                print("User ID: min. 4 letters, starts with a letter")
                secret = getpass(r"*Enter the secret : ")
            secret_verify = getpass("Confirm the secret : ")
            if secret != secret_verify:
                print("Secrets Mismatch! Retry.")
                secret = None
    else:
        get_secret(p2)

def get_credentials():
    p1 = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]{2,28}[a-zA-Z0-9]$')  # local variable to the function
    p2 = re.compile(r'^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+=\-[\]{};:\'",.<>?]{7,49}')  # local variable to the function
    global uid # declare uid as a global variable
    uid = input("Enter Network Admin ID : ")
    while not p1.match(uid):
        print("User ID: min. 4 letters, starts with a letter")
        uid = input(r"*Enter Network Admin ID : ")
    global pwd # declare pwd as a global variable
    pwd = None
    while not pwd:
        pwd = getpass("Enter Network Admin PWD : ")
        while not p2.match(pwd):
            print("Password: min. 7 chars, starts with a letter.")
            pwd = getpass(r"*Enter Network Admin PWD : ")
        pwd_verify = getpass("Confirm Network Admin PWD : ")
        if pwd != pwd_verify:
            print("Passwords Mismatch! Retry.")
            pwd = None 
    get_secret(p2) # Trigger get_secret function to run
    return uid, pwd, secret

get_credentials() # Trigger get_Credential function to run

def read_info(uid, pwd, secret):
    df = pd.read_csv(r'./devices_info.csv') # ensure the correct file location
    number_of_rows = len(df.index)
    # Read the values and save as a list, read column as df and save it as a list
    devicename = list(df['devicename'])
    device = list(df['device'])
    devicetype = list(df['devicetype'])
    ip = list(df['host'])
    newios = list(df['newios'])
    newiosmd5 = list(df['newiosmd5'])
    # Append the items and convert to a list, device_list
    global device_list # For md5_validate3.py
    device_list = []
    for index, rows in df.iterrows():
        device_append = [rows.devicename, rows.device, \
        rows.devicetype, rows.host, rows.newios, rows.newiosmd5]
        device_list.append(device_append)
    # Using device_list, create a netmiko friendly list device_list_netmiko
    global device_list_netmiko
    device_list_netmiko = []
    i = 0
    for x in device_list:
        print(x) # Check device info read
        if len(x) != 0: # As long as number of items in device_list is not 0 (empty)
            i += 1
            name = f'device{str(i)}' # Each for loop, the name is updated to device1, device2, device3, ...
            devicetype, host = x[2], x[3]
            device = {
            'device_type': devicetype,
            'host': host,
            'username': uid,
            'password': pwd,
            'secret': secret,
            }
            device_list_netmiko.append(device)

# Trigger read_info function to run
read_info(uid, pwd, secret)

def test_connectivity(device_list_netmiko):
    f1 = open('reachable_ips_ssh.txt', 'w+')
    f2 = open('reachable_ips_telnet.txt', 'w+')
    f3 = open('unreachable_ips.txt', 'w+')
    for device in device_list_netmiko:
        ip = device['host'].strip()
        print(ip)
        resp = os.system('ping -c 4 ' + ip)
        if resp == 0:
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
        else:
            print(f"{ip} unreachable")
            f3.write(f"{ip} unreachable\n")
    f1.close()
    f2.close()
    f3.close()

# Trigger test_connectivity function to run
test_connectivity(device_list_netmiko)

def validate_md5(device_list):
    for x in device_list:
        print(x[3], x[0], x[1], x[2])
        newios = x[4]
        newiosmd5 = str(x[5].lower()).strip()
        print(newiosmd5)
        newiosmd5hash = hashlib.md5()
        file = open(f'./new_ios/{newios}', 'rb')  # Update your IOS directory here
        content = file.read()
        newiosmd5hash.update(content)
        newiosmd5server = newiosmd5hash.hexdigest()
        print(newiosmd5server.strip())
        global newiossize
        newiossize = round(os.path.getsize(f'./new_ios/{newios}') / 1000000, 2)  # Update your IOS directory here
        print(newiossize, "MB")
        if newiosmd5server == newiosmd5:
            print("MD5 values matched!")
        else:
            print("Mismatched MD5 values. Exit")
            exit()
    return newiossize

# Trigger validate_md5 function to run
validate_md5(device_list)

def check_flash(device_list_netmiko, newiossize):
    for device in device_list_netmiko:
        ip = str(device['host'])
        net_connect = ConnectHandler(**device)
        net_connect.send_command("terminal length 0")
        showdir = net_connect.send_command("dir")
        # showflash = net_connect.send_command("show flash:") # For Cisco switches
        time.sleep(2)
        p1 = re.compile("\d+(?=\sbytes\sfree\))")
        m1 = p1.findall(showdir)
        flashfree = ((int(m1[0])/1000000))
        print(f"{ip} Free flash size : ", flashfree, "MB")
        if flashfree < (newiossize * 1.5):
            print(f"Not enough space on {ip}'s flash! Exiting")
            exit()
        else:
            print(f"{ip} has enough space for new IOS.")

# Trigger check_flash function to run
check_flash(device_list_netmiko, newiossize)

tt = time.mktime(time.localtime()) - t1
print("Total time : {0} seconds".format(tt)) # Timer finish to show total time (tt)