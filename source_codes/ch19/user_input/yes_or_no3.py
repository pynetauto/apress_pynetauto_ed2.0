def yes_or_no():
    user_input = input("Enter yes or no: ").lower()
    expected_response = ['yes', 'y', 'no', 'n']
    while user_input not in expected_response:
        user_input = input("Expecting yes or no: ").lower()
    if user_input == "yes" or user_input == "y":
        print("Oh Yes!")
    else:
        print("Oh No!")

yes_or_no()
