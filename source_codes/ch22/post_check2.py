from netmiko import ConnectHandler
import socket
import time
import difflib

destination_newios = "c8000v-universalk9.17.06.05a.SPA.bin"

device1 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.111',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}
device2 = {
    'device_type': 'cisco_xe',
    'host': '192.168.127.222',
    'username': 'jdoe',
    'password': 'cisco123',
    'secret': 'cisco123',
    'global_delay_factor': 2
}

devices_list = [device1, device2]

# Checks SSH port and then logs back in to complete the post-upgrade check.
def post_check():
    for device in devices_list:
        ip = str(device['host'])
        port = 22
        retry = 120
        delay = 10
        
        def isOpen(ip, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
            except:
                return False
            finally:
                s.close()
        
        t1 = time.mktime(time.localtime())
        ipup = False
        
        for i in range(retry):
            if isOpen(ip, port):
                ipup = True
                print(f"{ip} is online. Logging into device to perform post reload check")
                # Capture four show commands result from each router
                print("Performing post upgrade check.")
                net_connect = ConnectHandler(**device)
                net_connect.enable(cmd='enable 15')
                config_commands1 = ['no boot system', 'boot system flash:/' + destination_newios, 'do write memory']
                output = net_connect.send_config_set(config_commands1)
                print(output)
                net_connect.send_command('terminal length 0\n')
                
                with open(f'{ip}_showver_post.txt', 'w+') as f1:
                    print("Capturing post-reload 'show version'")
                    showver_post = net_connect.send_command("show version")
                    f1.write(showver_post)
                    time.sleep(1)
                
                with open(f'{ip}_showrun_post.txt', 'w+') as f2:
                    print("Capturing post-reload 'show running-config'")
                    showrun_post = net_connect.send_command("show running-config")
                    f2.write(showrun_post)
                    time.sleep(1)
                
                with open(f'{ip}_showint_post.txt', 'w+') as f3:
                    print("Capturing post-reload 'show ip interface brief'")
                    showint_post = net_connect.send_command("show ip interface brief")
                    f3.write(showint_post)
                    time.sleep(1)
                
                with open(f'{ip}_showroute_post.txt', 'w+') as f4:
                    print("Capturing post-reload 'show ip route'")
                    showroute_post = net_connect.send_command("show ip route")
                    f4.write(showroute_post)
                    time.sleep(1)
                
                # Compare pre vs post configurations
                showver_pre = "showver_pre"
                showver_post = "showver_post"
                showver_pre_lines = open(f"{ip}_showver_pre.txt").readlines()
                showver_post_lines = open(f"{ip}_showver_post.txt").readlines()
                difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showver_pre_lines, showver_post_lines, showver_pre, showver_post)
                difference_report = open(f"{ip}_show_ver_compared.html", "w+")
                difference_report.write(difference) # Writes the differences to html file
                difference_report.close()
                time.sleep(1)
                
                showrun_pre = "showrun_pre"
                showrun_post = "showrun_post"
                showrun_pre_lines = open(f"{ip}_showrun_pre.txt").readlines()
                showrun_post_lines = open(f"{ip}_showrun_post.txt").readlines()
                difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showrun_pre_lines, showrun_post_lines, showrun_pre, showrun_post)
                difference_report = open(f"{ip}_show_run_compared.html", "w+")
                difference_report.write(difference)
                difference_report.close()
                time.sleep(1)
                
                showint_pre = "showint_pre"
                showint_post = "showint_post"
                showint_pre_lines = open(f"{ip}_showint_pre.txt").readlines()
                showint_post_lines = open(f"{ip}_showint_post.txt").readlines()
                difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showint_pre_lines, showint_post_lines, showint_pre, showint_post)
                difference_report = open(f"{ip}_show_int_compared.html", "w+")
                difference_report.write(difference)
                difference_report.close()
                time.sleep(1)
                
                showroute_pre = "showroute_pre"
                showroute_post = "showroute_post"
                showroute_pre_lines = open(f"{ip}_showroute_pre.txt").readlines()
                showroute_post_lines = open(f"{ip}_showroute_post.txt").readlines()
                difference = difflib.HtmlDiff(wrapcolumn=70).make_file(showroute_pre_lines, showroute_post_lines, showroute_pre, showroute_post)
                difference_report = open(f"{ip}_show_route_compared.html", "w+")
                difference_report.write(difference)
                difference_report.close()
                time.sleep(1)
                
                break
            else:
                print("Device is still reloading. Please wait...")
                time.sleep(delay)
        
        t2 = time.mktime(time.localtime()) - t1
        print("Total wait time : {0} seconds".format(t2))
        print("=" * 80)
        time.sleep(1)

post_check()
print("All tasks completed. Check pre and post configuration comparison html files.")
