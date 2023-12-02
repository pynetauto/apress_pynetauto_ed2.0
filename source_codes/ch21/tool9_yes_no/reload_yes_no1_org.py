from netmiko import ConnectHandler
import time

destination_newios = "c8000v-universalk9.17.06.05a.SPA.bin"
newiosmd5 = "563797308a3036337c3dee9b4ab54649"

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.183.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}
device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.183.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}

devices_list = [device1, device2]
yes_list = ['yes', 'y']
no_list = ['no', 'n']

def yes_or_no():
    resp = input("Would you like to reload your devices? (y/n)? ").lower()
    if resp in yes_list:
        print("Reloading devices")
        for device in devices_list:
            ip = str(device['host'])
            net_connect = ConnectHandler(**device)
            net_connect.enable(cmd='enable 15')
            config_commands1 = ['no boot system', 'boot system flash:/' + destination_newios, 'do write memory']
            output = net_connect.send_config_set(config_commands1)
            print (output)
            net_connect.send_command('terminal length 0\n')
            show_boot = net_connect.send_command('show boot\n')
            show_dir = net_connect.send_command('dir\n')
            if destination_newios not in show_dir:
                print('Unable to locate new IOS on the flash:/. Exiting.')
                print("-"*80)
                exit()
            elif destination_newios not in show_boot:
                print('Boot system was not correctly configured. Exiting.')
                print("-"*80)
                exit()
            elif destination_newios in show_boot and destination_newios in show_dir:
                print(f'Found {destination_newios} in show boot')
                print("-"*80)
                net_connect.send_command("terminal length 0")
                time.sleep(1)
                with open(f'{ip}_showver_pre.txt', 'w+') as f1:
                    print("Capturing pre-reload 'show version'")
                    showver_pre = net_connect.send_command("show version")
                    f1.write(showver_pre)
                time.sleep(1)
                with open(f'{ip}_showrun_pre.txt', 'w+') as f2:
                    print("Capturing pre-reload 'show running-config'")
                    showrun_pre = net_connect.send_command("show running-config")
                    f2.write(showrun_pre)
                time.sleep(1)
                with open(f'{ip}_showint_pre.txt', 'w+') as f3:
                    print("Capturing pre-reload 'show ip interface brief'")
                    showint_pre = net_connect.send_command("show ip interface brief")
                    f3.write(showint_pre)
                time.sleep(1)
                with open(f'{ip}_showroute_pre.txt', 'w+') as f4:
                    print("Capturing pre-reload 'show ip route'")
                    showroute_pre = net_connect.send_command("show ip route")
                    f4.write(showroute_pre)
                time.sleep(1)
                print("-"*80)
                # Trigger the device reload
                print("Your device is now reloading.")
                net_connect.send_command('reload', expect_string='[confirm]')
                net_connect.send_command('yes\n')
                net_connect.send_command('\n')
                net_connect.disconnect()
                print("-"*80)
    elif resp in no_list:
        print("You have chosen to reload the devices later. Exiting the appliaiton.")
    else:
        yes_or_no()

yes_or_no()
print("All tasks completed.")
