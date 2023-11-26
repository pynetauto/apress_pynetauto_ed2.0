import pandas as pd

df = pd.read_csv(r'./devices_info.csv')
number_of_rows = len(df.index)

# Read the values and save as a list, read column as df and save it as a list
devicename = list(df['devicename'])
device = list(df['device'])
devicetype = list(df['devicetype'])
ip = list(df['host'])
newios = list(df['newios'])
newiosmd5 = list(df['newiosmd5'])

# Convert the list into a device_list
device_list = []
for index, rows in df.iterrows():
    device_append = [rows.devicename, rows.device, rows.devicetype, rows.host, rows.newios, rows.newiosmd5]
    device_list.append(device_append)

device_list_netmiko = []
i = 0
for x in device_list:
    if len(x) != 0:
        i += 1
        name = f'device{str(i)}'
        devicetype, host = x[2], x[3]
        device = {
            'device_type': devicetype,
            'host': host,
            'username': 'jdoe',
            'password': 'cisco123',
            'secret': 'cisco123',
        }
        device_list_netmiko.append(device)

print(device_list_netmiko)
