from netmiko import ConnectHandler

device_list_netmiko = [
    {'device_type': 'cisco_xe', 'host': '192.168.127.111', 'username': 'jdoe', 'password': 'cisco123', 'secret': 'cisco123'},
    {'device_type': 'cisco_xe', 'host': '192.168.127.222', 'username': 'jdoe', 'password': 'cisco123', 'secret': 'cisco123'}
]

def configure_aaa(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        config_commands = [
            'aaa new-model',
            'aaa authentication login default local enable',
            'aaa authorization exec default local'
        ]
        output = net_connect.send_config_set(config_commands)
        print(f"Configuration successful on {device['host']}:")
        print(output)
        net_connect.disconnect()
    except Exception as e:
        print(f"Failed to configure AAA on {device['host']}: {str(e)}")

def main():
    for device in device_list_netmiko:
        configure_aaa(device)

if __name__ == "__main__":
    main()
