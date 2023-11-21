# cpu_util_5min.py
import os
stream = os.popen('snmpwalk -v3  -l authPriv -u SNMPUser1 -a SHA -A "AUTHPass1"  -x AES -X "PRIVPass1" 192.168.127.3 1.3.6.1.4.1.9.9.109.1.1.1.1.5')
output = stream.read()
print(output)
