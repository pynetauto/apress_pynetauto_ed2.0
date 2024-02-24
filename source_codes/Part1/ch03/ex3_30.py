#ex3_30.py
import random

def aus_powerball():
    main_numbers = random.sample(range(1, 36), 5)  
    pb_number = random.randint(1, 20)
    print("Main numbers:", main_numbers)
    print("PowerBall number:", pb_number)

aus_powerball()