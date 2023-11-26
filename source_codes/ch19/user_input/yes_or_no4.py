from getpass import getpass

def get_credentials():
    username1 = input("Enter Network Admin1 ID: ")
    password1 = getpass("Enter Network Admin1 PWD: ")
    print("Username1:", username1, "Password1:", password1)

    yes_or_no = input("Network Admin2 credentials same as Network Admin1 credentials? (Yes/No): ").lower()
    expected_response = ['yes', 'y', 'no', 'n']
    while yes_or_no not in expected_response:
        yes_or_no = input("Expecting yes or no: ")

    if yes_or_no == "yes" or yes_or_no == "y":
        username2 = username1
        password2 = password1
        print("Username2:", username2, "Password2:", password2)
    else:
        username2 = input("Enter Network Admin2 ID: ")
        password2 = getpass("Enter Network Admin2 Password: ")
        print("Username2:", username2, "Password2:", password2)

get_credentials()
