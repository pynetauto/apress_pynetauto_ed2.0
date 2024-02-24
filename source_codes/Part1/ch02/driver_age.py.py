# driver_age.py
q1 = input ('What is your legal age? ')
age = int(q1)

if age < 16:
    print('You are too young to take a driving test.') 
elif age > 99:
    print('You are too old to take a driving test.') 
else:
    print('You\'re in the right age group to take a driving test.')