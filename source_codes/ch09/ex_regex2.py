import re

with open ("C:\\Users\\brend\\OneDrive\\Documents\\Intro_Py_Net_Auto_ed2_Working_Folder\\sh_ver.txt") as f:
    read_file = f.read()

# only match Cisco device model number from 'show version' output.
# Adding the 'r' prefix to treat the backslashes as literal characters and not as escape sequences
rtr_model = re.findall(r'C\d{4}[^\s]+', read_file)
router_model = rtr_model[0]
print(router_model)