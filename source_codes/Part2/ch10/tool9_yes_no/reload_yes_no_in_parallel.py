from netmiko import ConnectHandler
import threading
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

def show_clock(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f"Connecting to {device['host']}...")
        output = net_connect.send_command("show clock")
        print(f"Time on {device['host']}:")
        print(output)
        net_connect.disconnect()
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

def reload_devices(devices):
    threads = []
    for device in devices:
        thread = threading.Thread(target=reload_device, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    time.sleep(300)  # Sleep for 5 minutes

    threads = []
    for device in devices:
        thread = threading.Thread(target=show_clock, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    resp = input("Would you like to reload your devices? (y/n): ").lower()
    if resp == 'y':
        reload_devices(devices)
    elif resp == 'n':
        print("You chose not to reload the devices.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
    print("All tasks completed.")
