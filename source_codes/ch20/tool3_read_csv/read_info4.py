# read_info4.py
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
print(device_list)
