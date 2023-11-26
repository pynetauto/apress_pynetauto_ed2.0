from getpass import getpass
uid = input("Enter Network Admin ID : ")
pwd = getpass("Enter Network Admin PWD : ")
secret = getpass("Enter secret password : ")
print(uid, pwd, secret)
