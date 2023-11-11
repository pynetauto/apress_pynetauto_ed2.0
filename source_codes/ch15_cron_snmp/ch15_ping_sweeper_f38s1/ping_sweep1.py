import os
import datetime

with open("/home/jdoe/ch15_ping_sweeper/ip_addresses.txt", "r") as ip_addresses:
    print("-" * 80)
    print(datetime.datetime.now())
    for ip_add in ip_addresses:
        ip = ip_add.strip()
        rep = os.system('ping -c 3 ' + ip)
        if rep == 0:
            print(f"{ip} is reachable.")
        else:
            print(f"{ip} is either offline or ICMP is filtered.")

    print("-" * 80)
    print("All tasks completed.")
