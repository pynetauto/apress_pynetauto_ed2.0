import os

device_list = ['10.10.10.1', '192.168.127.111', '192.172.1.33', '192.168.127.222']

f1 = open('reachable_ips.txt', 'w+')
f2 = open('unreachable_ips.txt', 'w+')

for ip in device_list:
    if len(ip) != 0:
        print(f'Sending icmp packets to {ip}')
        resp = os.system('ping -c 3 ' + ip)
        if resp == 0:
            f1.write(f'{ip}\n')
            print('-' * 79)
        else:
            f2.write(f'{ip}\n')
            print('-' * 79)
    else:
        exit()

f1.close()
f2.close()
