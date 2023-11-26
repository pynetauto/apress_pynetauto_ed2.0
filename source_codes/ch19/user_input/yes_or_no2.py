def yes_or_no():
    user_input = input("Enter yes or no: ").lower()
    if user_input == "yes" or user_input == "y":
        print("Oh Yes!")
    elif user_input == "no" or user_input == "n":
        print("Oh No!")
    else:
        print("You have not entered the correct response.")

yes_or_no()
