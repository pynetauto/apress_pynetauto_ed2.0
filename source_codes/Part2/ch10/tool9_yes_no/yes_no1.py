yes = ['yes', 'y']
no = ['no', 'n']

def yes_or_no():
    resp = input("Would you like to reload your devices? (y/n)? ").lower()
    if resp in yes:
        print("YES")
    elif resp in no:
        print("NO")
    else:
        yes_or_no()

yes_or_no()

print("All tasks completed.")
