import os

device_list = ['192.168.127.111', '192.168.127.222']

for ip in device_list:
    if len(ip) != 0:
        print(f'Sending ICMP packets to {ip}')
        resp = os.system(f'ping -c 3 {ip}')
        if resp == 0:
            print(f'{ip} is on the network.')
            print('-' * 80)
        else:
            print(f'{ip} is unreachable.')
            print('-' * 80)
    else:
        exit()
