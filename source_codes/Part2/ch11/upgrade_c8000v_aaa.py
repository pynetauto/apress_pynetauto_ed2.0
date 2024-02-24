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
import threading # For multi-tasking using threads
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
        # print(x) # Ch22 Disabled: Final Test Run
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
        # print(ip) # Ch22 Disabled: Final Test Run
        resp = os.system('ping -c 4 ' + ip)
        if resp == 0:
            for port in range(22, 23):
                destination = (ip, port)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(3)
                        connection = s.connect(destination)
                        # print(f"{ip} {port} open") # Ch22 Disabled: Final Test Run
                        f1.write(f"{ip}\n")
                except:
                    # print(f"{ip} {port} closed") # Ch22 Disabled: Final Test Run
                    f3.write(f"{ip} {port} closed\n")
            for port in range(23, 24):
                destination = (ip, port)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(3)
                        connection = s.connect(destination)
                        # print(f"{ip} {port} open") # Ch22 Disabled: Final Test Run
                        f2.write(f"{ip}\n")
                except:
                    # print(f"{ip} {port} closed") # Ch22 Disabled: Final Test Run
                    f3.write(f"{ip} {port} closed\n")
        else:
            # print(f"{ip} unreachable") # Ch22 Disabled: Final Test Run
            f3.write(f"{ip} unreachable\n")
    f1.close()
    f2.close()
    f3.close()

# Trigger test_connectivity function to run
test_connectivity(device_list_netmiko)

def validate_md5(device_list):
    for x in device_list:
        # print(x[3], x[0], x[1], x[2]) # Ch22 Disabled: Final Test Run
        newios = x[4]
        newiosmd5 = str(x[5].lower()).strip()
        # print(newiosmd5) # Ch22 Disabled: Final Test Run
        newiosmd5hash = hashlib.md5()
        file = open(f'./new_ios/{newios}', 'rb')  # Update your IOS directory here
        content = file.read()
        newiosmd5hash.update(content)
        newiosmd5server = newiosmd5hash.hexdigest()
        # print(newiosmd5server.strip()) # Ch22 Disabled: Final Test Run
        global newiossize
        newiossize = round(os.path.getsize(f'./new_ios/{newios}') / 1000000, 2)  # Update your IOS directory here
        # print(newiossize, "MB") # Ch22 Disabled: Final Test Run
        if newiosmd5server == newiosmd5:
            # print("MD5 values matched!") # Ch22 Disabled: Final Test Run
            pass # Ch22 Added: Final Test Run
        else:
            # print("Mismatched MD5 values. Exit") # Ch22 Disabled: Final Test Run
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
        # print(f"{ip} Free flash size : ", flashfree, "MB") # Ch22 Disabled: Final Test Run
        if flashfree < (newiossize * 1.5):
            # print(f"Not enough space on {ip}'s flash! Exiting") # Ch22 Disabled: Final Test Run
            exit()
        else:
            # print(f"{ip} has enough space for new IOS.") # Ch22 Disabled: Final Test Run
            pass # Ch22 Added: Final Test Run

# Trigger check_flash function to run
check_flash(device_list_netmiko, newiossize)

t2 = time.mktime(time.localtime()) # Timer(t2) start for IOS uploading
# print("device_list_netmiko", device_list_netmiko) # Ch22 Disabled: Final Test Run
# print("device_list", device_list) # Ch22 Disabled: Final Test Run

def upload_ios(device, device_info):
    ip = device['host']
    username = device['username']
    newios = device_info[4]
    source_newios = f'./new_ios/{newios}'

    net_connect = ConnectHandler(**device)
    net_connect.send_command("terminal length 0")
    showrun = net_connect.send_command("show running-config")
    check_priv15 = f'username {username} privilege 15'
    aaa_authentication = "aaa authentication login default local enable"
    aaa_authorization = "aaa authorization exec default local"

    if check_priv15 in showrun and aaa_authentication in showrun and aaa_authorization in showrun:
        net_connect.enable(cmd='enable 15')
        net_connect.config_mode()
        net_connect.send_command('ip scp server enable')
        net_connect.exit_config_mode()
        time.sleep(1)
        print(f"New IOS uploading in progress to {ip}! Please wait...")
        scp_conn = SCPConn(net_connect)
        scp_conn.scp_transfer_file(source_newios, newios)
        scp_conn.close()
        time.sleep(1)
        net_connect.config_mode()
        net_connect.send_command('no ip scp server enable')
        net_connect.exit_config_mode()
        print(f"Upload to {ip} completed.")
    else:
        print(f"Failed to upload to {ip}. aaa authentication issues (or insufficient privileges)")
        response = input("Do you want to configure AAA settings? (y/n): ").lower()

        if response == 'y':
            net_connect.send_command("aaa new-model")
            net_connect.send_command("aaa authentication login default local enable")
            net_connect.send_command("aaa authorization exec default local")
            upload_ios(device, device_info) # Go back to the function to upload file
        else:
            print("Exiting without performing upload.")
            exit()  # Ch22 Added: Final Test Run

def ios_upload(device_list_netmiko, device_list):
    threads = []
    for device, device_info in zip(device_list_netmiko, device_list):
        thread = threading.Thread(target=upload_ios, args=(device, device_info))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # print("All file uploads completed.") # Ch22 Disabled: Final Test Run

# Trigger ios_upload() application.
ios_upload(device_list_netmiko, device_list)

def verify_ios_md5(device, device_info):
    ip = device['host']
    newios = device_info[4]
    newiosmd5 = device_info[5]
    net_connect = ConnectHandler(**device)

    try:
        locate_newios = net_connect.send_command(f"show flash: | in {newios}")
        if newios in locate_newios:
            result = net_connect.send_command(f"verify /md5 flash:{newios} {newiosmd5}")
            #print(f"Working on {ip}") # Ch22 Disabled: Final Test Run
            #print(result) # For Ch21, remove or keep it disabled
            p1 = re.compile(r'Verified')
            p2 = re.compile(r'[a-fA-F0-9]{31}[a-fA-F0-9]')
            verified = p1.findall(result)
            newiosmd5flash = p2.findall(result)
            if verified:
                result = True
                # print(f"{ip} - MD5 values MATCH! Continue") # Ch22 Disabled: Final Test Run
                # print("MD5 of new IOS on Server : ", newiosmd5) # Ch22 Disabled: Final Test Run
                # print("MD5 of new IOS on flash  : ", newiosmd5flash[0]) # Ch22 Disabled: Final Test Run
                return True
            else:
                result = False
                # print(f"{ip} - MD5 values DO NOT MATCH! Exiting.") # Ch22 Disabled: Final Test Run
                exit()
        else:
            print("No new IOS found on router's flash. Continue to next device...")
    except (NetMikoTimeoutException):
        print(f'Timeout error to : {ip}')
    except unknown_error:
        print('Unknown error occurred : ' + str(unknown_error))
    return False

def verify_md5(device_list_netmiko, device_list):
    for device in device_list_netmiko:
        device["read_timeout_override"] = 360 # changed this value to increase timeout to 6 minutes, routers take about 5 minutes to reload in my lab settings, adjust this time accordingly.
    # print(device_list_netmiko) # Ch22 Disabled: Final Test Run
    threads = []
    for device, device_info in zip(device_list_netmiko, device_list):
        thread = threading.Thread(target=verify_ios_md5, args=(device, device_info))
        thread.start()
        threads.append(thread)

verify_md5(device_list_netmiko, device_list)

def reload_device(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f"Reloading {device['host']}...")
        output = net_connect.send_command_timing("reload", strip_prompt=False, strip_command=False)
        if "confirm" in output:
            output += net_connect.send_command_timing("\n", strip_prompt=False, strip_command=False)
        if "Reload scheduled" in output:
            print(f"Reload command successful for {device['host']}")
        else:
            print(f"Reload command failed for {device['host']}")
        net_connect.disconnect()
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

def post_check(device):
    try:
        ip = device['host']
        net_connect = ConnectHandler(**device)
        net_connect.enable(cmd='enable 15')
        net_connect.send_command('terminal length 0\n')

        with open(f'{ip}_showver_post.txt', 'w+') as f1:
            # print("Capturing post-reload 'show version'") # Ch22 Disabled: Final Test Run
            showver_post = net_connect.send_command("show version")
            f1.write(showver_post)
            time.sleep(1)

        with open(f'{ip}_showrun_post.txt', 'w+') as f2:
            # print("Capturing post-reload 'show running-config'") # Ch22 Disabled: Final Test Run
            showrun_post = net_connect.send_command("show running-config")
            f2.write(showrun_post)
            time.sleep(1)

        with open(f'{ip}_showint_post.txt', 'w+') as f3:
            # print("Capturing post-reload 'show ip interface brief'") # Ch22 Disabled: Final Test Run
            showint_post = net_connect.send_command("show ip interface brief")
            f3.write(showint_post)
            time.sleep(1)

        with open(f'{ip}_showroute_post.txt', 'w+') as f4:
            # print("Capturing post-reload 'show ip route'") # Ch22 Disabled: Final Test Run
            showroute_post = net_connect.send_command("show ip route")
            f4.write(showroute_post)
            time.sleep(1)

        # Compare pre vs post configurations
        showver_pre = "showver_pre"
        showver_post = "showver_post"
        showver_pre_lines = open(f"{ip}_showver_pre.txt").readlines()
        showver_post_lines = open(f"{ip}_showver_post.txt").readlines()
        difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showver_pre_lines, showver_post_lines, showver_pre, showver_post)
        difference_report = open(f"{ip}_show_ver_compared.html", "w+")
        difference_report.write(difference) # Writes the differences to html file
        difference_report.close()
        time.sleep(1)

        showrun_pre = "showrun_pre"
        showrun_post = "showrun_post"
        showrun_pre_lines = open(f"{ip}_showrun_pre.txt").readlines()
        showrun_post_lines = open(f"{ip}_showrun_post.txt").readlines()
        difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showrun_pre_lines, showrun_post_lines, showrun_pre, showrun_post)
        difference_report = open(f"{ip}_show_run_compared.html", "w+")
        difference_report.write(difference)
        difference_report.close()
        time.sleep(1)

        showint_pre = "showint_pre"
        showint_post = "showint_post"
        showint_pre_lines = open(f"{ip}_showint_pre.txt").readlines()
        showint_post_lines = open(f"{ip}_showint_post.txt").readlines()
        difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showint_pre_lines, showint_post_lines, showint_pre, showint_post)
        difference_report = open(f"{ip}_show_int_compared.html", "w+")
        difference_report.write(difference)
        difference_report.close()
        time.sleep(1)

        showroute_pre = "showroute_pre"
        showroute_post = "showroute_post"
        showroute_pre_lines = open(f"{ip}_showroute_pre.txt").readlines()
        showroute_post_lines = open(f"{ip}_showroute_post.txt").readlines()
        difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showroute_pre_lines, showroute_post_lines, showroute_pre, showroute_post)
        difference_report = open(f"{ip}_show_route_compared.html", "w+")
        difference_report.write(difference)
        difference_report.close()
        time.sleep(1)

    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

def reload_devices(device_list_netmiko):
    threads = []
    for device in device_list_netmiko:
        thread = threading.Thread(target=reload_device, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

#    time.sleep(120)  # Sleep for 2 minutes, use this sleep timer to add more delays for router reboot as needed

    threads = []
    for device in device_list_netmiko:
        thread = threading.Thread(target=post_check, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Function to capture show command outputs before device reload
def show_and_capture(device):
    ip = device['host']
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        with open(f'{ip}_showver_pre.txt', 'w+') as f1:
            showver_pre = net_connect.send_command("show version")
            f1.write(showver_pre)
            time.sleep(1)
        with open(f'{ip}_showrun_pre.txt', 'w+') as f2:
            showrun_pre = net_connect.send_command("show running-config")
            f2.write(showrun_pre)
            time.sleep(1)
        with open(f'{ip}_showint_pre.txt', 'w+') as f3:
            showint_pre = net_connect.send_command("show ip interface brief")
            f3.write(showint_pre)
            time.sleep(1)
        with open(f'{ip}_showroute_pre.txt', 'w+') as f4:
            showroute_pre = net_connect.send_command("show ip route")
            f4.write(showroute_pre)
            time.sleep(1)
        net_connect.disconnect()
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

# Function to run threads for each device
def run_show_and_capture(device_list_netmiko):
    threads = []
    for device in device_list_netmiko:
        thread = threading.Thread(target=show_and_capture, args=(device,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def change_boot_var(device, device_info):
    ip = device['host']
    newios = device_info[4]
    net_connect = ConnectHandler(**device)

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable(cmd='enable 15')
        config_commands1 = ['no boot system', 'boot system flash:/' + newios, 'do write memory']
        output = net_connect.send_config_set(config_commands1)
        print(output)
    except (NetMikoTimeoutException):
        print(f'Timeout error to : {ip}')
    except unknown_error:
        print('Unknown error occurred : ' + str(unknown_error))
    return False

def run_change_boot_var(device_list_netmiko, device_list):
    # print(device_list_netmiko) # Ch22 Disabled: Final Test Run
    threads = []
    for device, device_info in zip(device_list_netmiko, device_list):
        thread = threading.Thread(target=change_boot_var, args=(device, device_info))
        thread.start()
        threads.append(thread)

def reload_yes_no_in_parallel(device_list_netmiko, device_list):
    time.sleep(10)
    # Run the threads using the function
    run_show_and_capture(device_list_netmiko)
    resp = input("Would you like to reload your devices? (y/n): ").lower()
    if resp == 'y':
        # Change the boot variable to new IOS version
        run_change_boot_var(device_list_netmiko, device_list)
        # Run the router reload command
        reload_devices(device_list_netmiko)
    elif resp == 'n':
        print("You chose not to reload the devices.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

time.sleep(10)
reload_yes_no_in_parallel(device_list_netmiko, device_list)

tt_ios_upload = time.mktime(time.localtime()) - t2
print("Total IOS Upload Time : {0} seconds".format(tt_ios_upload)) # Time taken to upload IOS file

tt = time.mktime(time.localtime()) - t1
print("Total time to run Application : {0} seconds".format(tt)) # Timer finish to show total time (tt)
