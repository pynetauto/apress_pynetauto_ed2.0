from netmiko import ConnectHandler
import time

destination_newios = "c8000v-universalk9.17.06.05a.SPA.bin"
# newiosmd5 = "563797308a3036337c3dee9b4ab54649"

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2  # Used to slow down the script
}
device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}
devices_list = [device1, device2]
# yes_list = ['yes', 'y'] # used in yes_no1.py
# no_list = ['no', 'n'] # used in yes_no1.py

def reload_device(device):
    ip = str(device['host'])
    net_connect = ConnectHandler(**device)
    net_connect.enable(cmd='enable 15')
    config_commands1 = ['no boot system', 'boot system flash:/' + destination_newios, 'do write memory']
    output = net_connect.send_config_set(config_commands1)
    print(output)
    net_connect.send_command('terminal length 0\n')
    show_boot = net_connect.send_command('show boot\n')
    show_dir = net_connect.send_command('dir\n')
    if destination_newios not in show_dir:
        print(f'Unable to locate new IOS on the flash: {ip}. Exiting.')
        print("-" * 80)
        raise Exception("IOS not found")
    elif destination_newios not in show_boot:
        print(f'Boot system was not correctly configured on {ip}. Exiting.')
        print("-" * 80)
        raise Exception("Boot system misconfiguration")
    elif destination_newios in show_boot and destination_newios in show_dir:
        print(f'Found {destination_newios} in show boot on {ip}')
        print("-" * 80)
        net_connect.send_command("terminal length 0")
        time.sleep(1)
        with open(f'{ip}_showver_pre.txt', 'w+') as f1:
            print(f"Capturing pre-reload 'show version' on {ip}")
            showver_pre = net_connect.send_command("show version")
            f1.write(showver_pre)
            time.sleep(1)
        with open(f'{ip}_showrun_pre.txt', 'w+') as f2:
            print(f"Capturing pre-reload 'show running-config' on {ip}")
            showrun_pre = net_connect.send_command("show running-config")
            f2.write(showrun_pre)
            time.sleep(1)
        with open(f'{ip}_showint_pre.txt', 'w+') as f3:
            print(f"Capturing pre-reload 'show ip interface brief' on {ip}")
            showint_pre = net_connect.send_command("show ip interface brief")
            f3.write(showint_pre)
            time.sleep(1)
        with open(f'{ip}_showroute_pre.txt', 'w+') as f4:
            print(f"Capturing pre-reload 'show ip route' on {ip}")
            showroute_pre = net_connect.send_command("show ip route")
            f4.write(showroute_pre)
            time.sleep(1)
        print("-" * 80)
        # Trigger the device reload
        print(f"Your device {ip} is now reloading.")
        net_connect.send_command('reload', expect_string='[confirm]')
        net_connect.send_command('yes\n')
        net_connect.send_command('\n')
        net_connect.disconnect()
        print("-" * 80)

# Updated function to prompt user for reload decision
def yes_or_no():
    valid_responses = {'yes': True, 'y': True, 'no': False, 'n': False}
    while True:
        resp = input("Would you like to reload your devices? (y/n)? ").lower()
        if resp in valid_responses:
            user_choice = valid_responses[resp]
            if user_choice:
                print("Reloading devices")
                for device in devices_list:
                    try:
                        reload_device(device)
                    except Exception as e:
                        print(f"Exception occurred for {device['host']}: {e}")
            else:
                print("You have chosen to reload the devices later. Exiting the application.")
            break
        print("Please enter 'yes' or 'no'.")

yes_or_no()
print("All tasks completed.")
