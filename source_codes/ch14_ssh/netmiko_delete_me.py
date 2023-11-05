#!/usr/bin/env python3
import re
from netmiko import ConnectHandler
from getpass import getpass
import time
device1 = {
'device_type': 'cisco_ios',
'ip': input('IP Address : '),
'username': input('Enter username : '),
'password': getpass('SSH password : '),
}
net_connect = ConnectHandler(**device1)
net_connect.send_command("terminal length 0\n")
time.sleep(1)
dir_flash = net_connect.send_command("dir flash:\n")
print(dir_flash)
p30 = re.compile(r'D[0-9a-zA-Z]{4}.*.bin')
m30 = p30.search(dir_flash)
time.sleep(1)
if bool(m30) == True:
    print("If you can see 'Delete_me.bin' file, select it and press Enter.")
    del_cmd = "del flash:/"
    old_ios = input("*Old IOS (bin) file to delete : ")
    while not p30.match(old_ios) or old_ios not in dir_flash:
        old_ios = input("**Old IOS (bin) file to delete : ")
    command = del_cmd + old_ios
    output = net_connect.send_command_timing(
        command_string=command,
        strip_prompt=False,
        strip_command=False
    )
    if "Delete filename" in output:
        output += net_connect.send_command_timing(
            command_string="\n",
            strip_prompt=False,
            strip_command=False
        )
    if "confirm" in output:
        output += net_connect.send_command_timing(
            command_string="y",
            strip_prompt=False,
            strip_command=False
        )
    net_connect.disconnect
    print(output)
elif bool(m30) == False:
    print("No IOS file under 'flash:/', select the directory to view.")
    open_dir = input("*Enter Directory name : ")
    while not open_dir in dir_flash:
        open_dir = input("** Enter Directory name : ")
    open_dir_cmd = (r"dir flash:/" + open_dir)
    send_open_dir = net_connect.send_command(open_dir_cmd)
    print(send_open_dir)
    p31 = re.compile(r'D[0-9a-zA-Z]{4}.*.bin')
    m31 = p31.search(send_open_dir)
    if bool(m31) == True:
        print("If you see old IOS (bin) in the directory. Select it and press Enter.")
        del_cmd = "del flash:/" + open_dir + "/"
        old_ios = input("*Old IOS (bin) file to delete : ")
        while not p30.match(old_ios) or old_ios not in send_open_dir:
            old_ios = input("**Old IOS (bin) file to delete : ")
        command = del_cmd + old_ios
        output = net_connect.send_command_timing(
            command_string=command,
            strip_prompt=False,
            strip_command=False
        )
        if "Delete filename" in output:
            output += net_connect.send_command_timing(
                command_string="\n",
                strip_prompt=False,
                strip_command=False
            )
        if "confirm" in output:
            output += net_connect.send_command_timing(
                command_string="y",
                strip_prompt=False,
                strip_command=False
            )
        net_connect.disconnect
        print(output)
    else:
        ("No IOS found.")
        exit()
    net_connect.disconnect
