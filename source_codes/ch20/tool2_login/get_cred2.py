from getpass import getpass

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
        secret_verify = getpass("Confirm the secret : ")
        if secret != secret_verify:
            print("! Secrets do not match. Please try again.")
            secret = None
        else:
            get_secret()

def get_credentials():
    global uid
    uid = input("Enter Network Admin ID : ")
    global pwd
    pwd = None
    while not pwd:
        pwd = getpass("Enter Network Admin PWD : ")
        pwd_verify = getpass("Confirm Network Admin PWD : ")
        if pwd != pwd_verify:
            print("! Network Admin Passwords do not match. Please try again.")
            pwd = None
        get_secret()
        return uid, pwd, secret

get_credentials()
print(uid, pwd, secret)
