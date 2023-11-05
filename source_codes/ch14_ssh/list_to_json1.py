import json

devices = [
    {
        'ip_address': '192.168.127.3',
        'vendor': 'cisco',
        'username': 'jdoe',
        'password': 'cisco123'
    },
    {
        'ip_address': '192.168.127.4',
        'vendor': 'cisco',
        'username': 'jdoe',
        'password': 'cisco123'
    },
    {
        'ip_address': '192.168.127.101',
        'vendor': 'cisco',
        'username': 'jdoe',
        'password': 'cisco123'
    },
    {
        'ip_address': '192.168.127.102',
        'vendor': 'cisco',
        'username': 'jdoe',
        'password': 'cisco123'
    },
    {
        'ip_address': '192.168.127.133',
        'vendor': 'cisco',
        'username': 'jdoe',
        'password': 'cisco123'
    }
]

json_devices = json.dumps(devices, indent=4)
print(json_devices)
