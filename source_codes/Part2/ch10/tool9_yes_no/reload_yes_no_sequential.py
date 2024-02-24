from netmiko import ConnectHandler
import time

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.127.111',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123',
        'global_delay_factor': 3,
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.127.222',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123',
        'global_delay_factor': 3,
    },
    # Add more devices as needed
]

def show_clock(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f"Connecting to {device['host']}...")
        output = net_connect.send_command("show clock")
        print(f"Time on {device['host']}:\n{output}\n")
        net_connect.disconnect()
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

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

def main():
    for device in devices:
        show_clock(device)

    for device in devices:
        reload_device(device)

    print("Routers rebooting... Waiting for the reboot to complete.")
    time.sleep(300)  # Wait for 5 minutes for the routers to reboot

    print("Disconnected from routers after reboot.")

    for device in devices:
        try:
            net_connect = ConnectHandler(**device)
            net_connect.disconnect()
            print(f"Disconnected from {device['host']}")
        except Exception as e:
            print(f"Error disconnecting from {device['host']}: {e}")

    print("Waiting before reconnecting...")
    time.sleep(10)  # Wait a few seconds before reconnecting

    print("Reconnecting to devices and initiating another reboot.")
    for device in devices:
        reload_device(device)

if __name__ == "__main__":
    main()
    print("All tasks completed.")
