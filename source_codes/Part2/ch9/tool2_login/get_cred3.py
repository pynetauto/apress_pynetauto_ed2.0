import re
from getpass import getpass

p1 = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{3,28}[a-zA-Z0-9]$')
p2 = re.compile(r'^[a-zA-Z].{7,49}')

def get_secret():
    global secret
    resp = input("Is secret the same as password? (y/n) : ")
    resp = resp.lower()
    if resp == "yes" or resp == "y":
        secret = pwd
    elif resp == "no" or resp == "n":
        secret = None
    while not secret:
        secret = getpass("Enter the secret : ")
        while not p2.match(secret):
            secret = getpass(r"*Enter the secret : ")
        secret_verify = getpass("Confirm the secret : ")
        if secret != secret_verify:
            print("!!! secret do not match. Please try again.")
            secret = None
        else:
            get_secret()

def get_credentials():
    global uid
    uid = input("Enter Network Admin ID : ")
    while not p1.match(uid):
        uid = input(r"*Enter Network Admin ID : ")
    global pwd
    pwd = None
    while not pwd:
        pwd = getpass("Enter Network Admin PWD : ")
        while not p2.match(pwd):
            pwd = getpass(r"*Enter Network Admin PWD : ")
        pwd_verify = getpass("Confirm Network Admin PWD : ")
        if pwd != pwd_verify:
            print("!!! Network Admin Passwords do not match. Please try again.")
            pwd = None
        get_secret()
    return uid, pwd, secret

get_credentials()
print(uid, pwd, secret)
