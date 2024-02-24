from netmiko import ConnectHandler
import threading
import time

# List of devices to perform operations on
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.127.111',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123',
        'global_delay_factor': 2,
        'timeout' : 0,
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.127.222',
        'username': 'jdoe',
        'password': 'cisco123',
        'secret': 'cisco123',
        'global_delay_factor': 2,
        'timeout' : 0,
    },
    # ... Add more devices as needed
]

# Function to capture show command outputs before device reload
def show_and_capture(device):
    ip = str(device['host'])
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        # Capturing 'show' commands before reload
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
        # ... Add more show commands to capture as needed
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

# Function to reload an individual device
def reload_device(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        # Reload the device
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

# Function to display the current time on a device
def show_clock(device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        # Display the current time
        output = net_connect.send_command("show clock")
        print(f"Time on {device['host']}:")
        print(output)
        net_connect.disconnect()
    except Exception as e:
        print(f"Connection error with {device['host']}: {e}")

# Function to reload the devices
def reload_devices(devices):

    threads = []
    # Capture 'show' commands before reloading devices
    for device in devices:
        print(f"{device['host']} running show commands and capture")
        thread = threading.Thread(target=show_and_capture, args=(device,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    threads = []
    # Show current time on device before the reload
    for device in devices:
        print(f"{device['host']} Showing time after routers has been reloaded")
        thread = threading.Thread(target=show_clock, args=(device,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    threads = []
    # Reload devices
    for device in devices:
        print(f"{device['host']} Reloading the device")
        thread = threading.Thread(target=reload_device, args=(device,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    time.sleep(240)  # Sleep for 5 minutes, until the routers reload and normalize
    threads = []
    # Show current time on device after the reload
    for device in devices:
        print(f"{device['host']} Showing time after routers has been reloaded")
        thread = threading.Thread(target=show_clock, args=(device,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

# Main function to initiate operations based on user input
def main():
    yes = ['yes', 'y']
    no = ['no', 'n']
    resp = input("Would you like to reload your devices? (y/n): ").lower()
    if resp in yes:
        reload_devices(devices)
    elif resp in no:
        print("You chose not to reload the devices.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        main()

if __name__ == "__main__":
    main()
    print("All tasks completed.")
