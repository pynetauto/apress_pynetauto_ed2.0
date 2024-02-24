from getpass import getpass

def get_credentials():
    username1 = input("Enter Network Admin1 ID: ")
    password1 = None
    while not password1:
        password1 = getpass("Enter Network Admin1 PWD : ")
        password1_verify = getpass("Confirm Network Admin1 PWD : ")
        if password1 != password1_verify:
            print("Passwords do not match. Please try again.")
            password1 = None
    print("Username1 :", username1, "Password1 :", password1)

    yes_or_no = input("Network Admin2 credentials same as Network Admin1 credentials? (Yes/No): ").lower()
    expected_response = ['yes', 'y', 'no', 'n']
    while yes_or_no not in expected_response:
        yes_or_no = input("Expecting yes or no : ")

    if yes_or_no == "yes" or yes_or_no == "y":
        username2 = username1
        password2 = password1
        print("Username2 :", username2, "Password2 :", password2)
    else:
        username2 = input("Enter Network Admin2 ID: ")
        password2 = None
        while not password2:
            password2 = getpass("Enter Network Admin2 PWD : ")
            password2_verify = getpass("Confirm Network Admin2 PWD : ")
            if password2 != password2_verify:
                print("Passwords do not match. Please try again.")
                password2 = None
        print("Username2 :", username2, "Password2 :", password2)

get_credentials()
