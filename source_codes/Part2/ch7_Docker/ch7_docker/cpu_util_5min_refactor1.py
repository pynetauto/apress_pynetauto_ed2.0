from twilio.rest import Client
import os
import re
import time
from time import strftime

current_time = strftime("%a, %d %b %Y %H:%M:%S")
account_sid = "AC42d8ee3a2ee22e8684e6f3d4eca2b8c7"
auth_token = "5233e8502a3dd3a2d006913c937a6f26"
my_smartphone = "+61490417510"
twilio_trial = "+16076003338"

def send_sms():
   client = Client(account_sid, auth_token)
   my_message = f"High CPU utilization notice, R2 has reached 90% CPU utilization."
   message = client.messages.create(body=my_message, from_=twilio_trial, to=my_smartphone)
   print(message.sid)

stream = os.popen('snmpwalk -v3 -l authPriv -u SNMPUser1 -a SHA -A "AUTHPass1"  -x AES -X "PRIVPass1" 192.168.127.3 1.3.6.1.4.1.9.9.109.1.1.1.1.5')
output = stream.read()
time.sleep(3)
print("-"*80)
print(current_time, output)

with open('./cpu_oid_log.txt', 'a+') as f:
   if "Gauge32:" in output:
      p1 = re.compile(r"(?:Gauge32: )(\d+)")
      m1 = p1.findall(output)
      cpu_util_value = m1[0]

      if int(cpu_util_value) < 90:
         f.write(f"{current_time} {cpu_util_value}%, OK\n")
         print("OK")
      elif int(cpu_util_value) >= 90:
         f.write(f"{current_time} {cpu_util_value}%, High CPU\n")
         print("High CPU")
         send_sms()

   elif "Timeout:" in output:
      f.write(f"{current_time} High CPU, Timeout: No Response\n")
      print("Timeout: No Response")
      send_sms()

   elif "snmpwalk:" in output:
      f.write(f"{current_time} High CPU, snmpwalk: Timeout\n")
      print("No Response")
      send_sms()

   else:
      f.write(f"{current_time} High CPU utilization, IndexError\n")
      print("IndexError occurred due to High CPU Utilization")
      send_sms()

print("Finished")
