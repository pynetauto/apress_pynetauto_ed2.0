from netmiko import ConnectHandler

# Device information
device1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

device2 = {
    'device_type': 'cisco_ios',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123'
}

devices_list = [device1, device2]

for device in devices_list:
    net_connect = ConnectHandler(**device)
    net_connect.enable()

    # AAA configurations
    commands = [
        'aaa new-model',
        'aaa authentication login default local enable'
    ]

    output = net_connect.send_config_set(commands)
    print(output)

    # Save configuration
    save_output = net_connect.save_config()
    print(save_output)

    net_connect.disconnect()
