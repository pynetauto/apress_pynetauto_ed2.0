# cpu_util_5min.py
import os
import re

stream = os.popen('snmpwalk -v3  -l authPriv -u SNMPUser1 -a SHA -A "AUTHPass1"  -x AES -X "PRIVPass1" 192.168.127.3 1.3.6.1.4.1.9.9.109.1.1.1.1.5')
output = stream.read()
print(output)
p1 = re.compile(r"(?:Gauge32: )(\d+)")
m1 = p1.findall(output)
cpu_util_value = int(m1[0])
print(cpu_util_value) 
