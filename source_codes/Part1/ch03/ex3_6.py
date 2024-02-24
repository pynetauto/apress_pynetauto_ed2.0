import re

name = input("Enter your name: ")
while True:
    while not re.match("^[a-zA-Z]+$", name):
        name = input("Enter your name: ")
    else:
        print(name)
        exit()