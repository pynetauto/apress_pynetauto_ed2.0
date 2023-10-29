import getpass
import telnetlib
HOST = "192.168.127.101"
user = input("Enter your username: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
       tn.read_until(b"Password: ")
       tn.write(password.encode('ascii') + b"\n")
# Get into config mode
tn.write(b"conf t\n")
# configure 4 VLANs with VLAN names
tn.write(b"vlan 2\n")
tn.write(b"name Data_vlan_2\n")
tn.write(b"vlan 3\n")
tn.write(b"name Data_vlan_3\n")
tn.write(b"vlan 4\n")
tn.write(b"name Voice_vlan_4\n")
tn.write(b"vlan 5\n")
tn.write(b"name Wireless_vlan_5\n")
tn.write(b"exit\n")
# configure Gi1/0 - Gi1/3 as access siwtchports and assign vlan 5 for wireless APs
tn.write(b"interface range gi1/0 - 3\n")
tn.write(b"switchport mode access\n")
tn.write(b"switchport access vlan 5\n")
tn.write(b"no shut\n")
#configure gi2/0 - gi2/3 as access switchports and assign vlan 2 for data and vlan 4 for voice
tn.write(b"interface range gi2/0 - 3\n")
tn.write(b"switchport mode access \n")
tn.write(b"switchport access vlan 2\n")
tn.write(b"switchport voice vlan 4\n")
tn.write(b"no shut\n")
tn.write(b"end\n")
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))
