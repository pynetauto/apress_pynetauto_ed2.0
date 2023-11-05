from getpass import getpass

def get_credentials():
    username = input("*Enter Network Admin ID : ")
    password = None
    while not password:
        password = getpass("*Enter Network Admin PWD : ")
        password_verify = getpass("**Confirm Network Admin PWD : ")
        if password != password_verify:
            print("! Network Admin Passwords do not match. Please try again.")
            password = None
    print(username, password)
    return username, password

get_credentials()
