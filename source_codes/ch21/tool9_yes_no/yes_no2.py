def yes_or_no():
    valid_responses = {'yes': True, 'y': True, 'no': False, 'n': False}
    while True:
        resp = input("Would you like to reload your devices? (y/n)? ").lower()
        if resp in valid_responses:
            return valid_responses[resp]
        print("Please enter 'yes' or 'no'.")

user_choice = yes_or_no()

if user_choice:
    print("You have chosen to reload your devices.")
else:
    print("You chose not to reload the devices.")

print("All tasks completed.")
