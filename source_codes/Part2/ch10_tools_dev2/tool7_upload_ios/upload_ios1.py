import time
from netmiko import ConnectHandler, SCPConn

source_newios = "/home/jdoe/ch10_tools_dev2/new_ios/c8000v-Dev-File-Only.bin"
destination_newios = "c8000v-Dev-File-Only.bin"

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

devices_list = [device1, device2]

for device in devices_list:
    ip = str(device['host'])
    username = str(device['username'])
    net_connect = ConnectHandler(**device)
    net_connect.send_command("terminal length 0")
    showrun = net_connect.send_command("show running-config")
    check_priv15 = (f'username {username} privilege 15')
    aaa_authenication = "aaa authentication login default local enable"
    aaa_authorization = "aaa authorization exec default local"

    if check_priv15 in showrun:
        print(f"{username} has level 15 privilege - OK")
        if aaa_authenication in showrun:
            print("check_aaa_authentication - OK")
            if aaa_authorization in showrun:
                print("check_aaa_authorization - OK")
            else:
                print("aaa_authorization - FAILED ")
                exit()
        else:
            print("aaa_authentication - FAILED ")
            exit()
    else:
        print(f"{username} has not enough privilege - FAILED")
        exit()

    net_connect.enable(cmd='enable 15')
    net_connect.config_mode()
    net_connect.send_command('ip scp server enable')
    net_connect.exit_config_mode()
    time.sleep(1)
    print("New IOS uploading in progress! Please wait...")
    scp_conn = SCPConn(net_connect)
    scp_conn.scp_transfer_file(source_newios, destination_newios)
    scp_conn.close()
    time.sleep(1)
    net_connect.config_mode()
    net_connect.send_command('no ip scp server enable')
    net_connect.exit_config_mode()
    print("-"*80)
