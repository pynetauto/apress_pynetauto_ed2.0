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
print(devicename)
print(device)
print(devicetype)
print(ip)
print(newios)
print(newiosmd5)
