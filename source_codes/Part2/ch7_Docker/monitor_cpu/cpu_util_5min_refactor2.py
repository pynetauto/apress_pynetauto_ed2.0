from twilio.rest import Client
import subprocess
import re
from time import strftime, sleep

current_time = strftime("%a, %d %b %Y %H:%M:%S")
account_sid = "ACd4a53a28d711420bd6ee19c67ea477e7"
auth_token = "ef861c2130126cb336292230741cb52a "
my_smartphone = "+61490417510"
twilio_trial = "+13095884935"

def send_sms(message):
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_trial, to=my_smartphone)

def get_cpu_util():
    cmd = 'snmpwalk -v3 -l authPriv -u SNMPUser1 -a SHA -A "AUTHPass1"  -x AES -X "PRIVPass1" 192.168.127.3 1.3.6.1.4.1.9.9.109.1.1.1.1.5'
    output = subprocess.getoutput(cmd)
    return output

def log_and_notify(message):
    with open('./cpu_oid_log.txt', 'a+') as f:
        f.write(f"{current_time} {message}\n")
    send_sms(message)

def monitor_cpu():
    output = get_cpu_util()
    print("-" * 80)
    print(current_time, output)

    if "Gauge32:" in output:
        cpu_util_match = re.search(r"(?:Gauge32: )(\d+)", output)
        if cpu_util_match:
            cpu_util_value = cpu_util_match.group(1)
            if int(cpu_util_value) >= 90:
                log_and_notify(f"{cpu_util_value}%, High CPU")
                print("High CPU")
            else:
                print("OK")
        else:
            log_and_notify("Error: Unable to parse CPU utilization value")
            print("Error: Unable to parse CPU utilization value")
    elif "Timeout:" in output:
        log_and_notify("High CPU, Timeout: No Response")
        print("Timeout: No Response")
    elif "snmpwalk:" in output:
        log_and_notify("High CPU, snmpwalk: Timeout")
        print("No Response")
    else:
        log_and_notify("High CPU utilization, IndexError")
        print("IndexError occurred due to High CPU Utilization")

    print("Finished")

monitor_cpu()
