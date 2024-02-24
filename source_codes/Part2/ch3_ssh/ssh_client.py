# Base ssh_client.py code borrowed from the following site:
# URL: https://gist.github.com/ghawkgu/944017
#!/usr/bin/env python

import paramiko

hostname = 'localhost'
port = 22
username = 'foo'
password = 'xxxYYYxxx'

if __name__ == "__main__":
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(hostname, port, username, password)
    stdin, stdout, stderr = s.exec_command('ifconfig')
    print stdout.read()
    s.close()
