import pymysql
import login
import random
from database import cur,conn


print('''Welcome to MioKumud...
Press:-
1.Products
2.Login/Signup
''')
while True:
    action = input("Select your action: ").strip()

    if (action == '1'):
        login.view_products(cur)
    if (action == '2'):
        print('''Press:-
            1. Phone
            2. Email
                ''')
        signup_by = input('Please enter: ')
        if (signup_by == '1'):
            result = login.signup_phone(cur)
            if result:
                signup_complete, user_details = result
                print(user_details)
        if (signup_by == '2'):
            result = login.signup_email(cur)
            if result:
                signup_complete, user_details = result
                print(user_details)
    if (action == '0'):
        print('Thanks')
        break





