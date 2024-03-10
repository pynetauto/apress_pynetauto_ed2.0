import pandas as pd
import os.path
import hashlib

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
    device_append = [rows.devicename, rows.device, \
    rows.devicetype, rows.host, rows.newios, rows.newiosmd5]
    device_list.append(device_append)

for x in device_list:
    print(x[0])
    newios = x[4]
    newiosmd5 = x[5].lower()
    newiosmd5hash = hashlib.md5()
    file = open(f'/home/jdoe/ch9_tools_dev1/new_ios/{newios}', 'rb')
    content = file.read()
    newiosmd5hash.update(content)
    newiosmd5server = newiosmd5hash.hexdigest()
    print(newiosmd5server)
    newiossize = round(os.path.getsize(f'/home/jdoe/ch9_tools_dev1/new_ios/{newios}')/1000000,2)
    print(newiossize, "MB")
