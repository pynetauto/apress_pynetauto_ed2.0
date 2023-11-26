import os

device_list = ['10.10.10.1', '192.168.127.111', '192.172.1.33', '192.168.127.222']

reachable_ips = []
unreachable_ips = []

for ip in device_list:
    if len(ip) != 0:
        print(f'Sending icmp packets to {ip}')
        resp = os.system(f'ping -c 3 {ip}')
        if resp == 0:
            reachable_ips.append(ip)
            print('-' * 79)
        else:
            unreachable_ips.append(ip)
            print('-' * 79)
    else:
        exit()

print("Reachable IPs: ", reachable_ips)
print("Unreachable IPs: ", unreachable_ips)
