from netmiko import ConnectHandler
import getpass

def get_credentials():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    secret = getpass.getpass("Enter secret: ")
    return username, password, secret

device_list_netmiko = [
    {'device_type': 'cisco_xe', 'host': '192.168.127.111'},
    {'device_type': 'cisco_xe', 'host': '192.168.127.222'}
]

def configure_aaa(device, username, password, secret):
    try:
        device['username'] = username
        device['password'] = password
        device['secret'] = secret

        net_connect = ConnectHandler(**device)
        net_connect.enable()
        config_commands = [
            'aaa new-model',
            'aaa authentication login default local enable',
            'aaa authorization exec default local'
        ]
        output = net_connect.send_config_set(config_commands)

        # Save configuration after applying AAA configuration
        save_config = net_connect.save_config()

        print(f"Configuration successful on {device['host']}:")
        print(output)
        print(save_config)
        net_connect.disconnect()
    except Exception as e:
        print(f"Failed to configure AAA on {device['host']}: {str(e)}")

def main():
    username, password, secret = get_credentials()
    for device in device_list_netmiko:
        configure_aaa(device, username, password, secret)

if __name__ == "__main__":
    main()
