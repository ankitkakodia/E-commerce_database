import pymysql
import login
import random
from database import cur,conn
while True:
    new_phone = input("Please enter phone: ").strip()
    if (len(new_phone)== 10):
        select = f"select phone from users where phone = '{new_phone}';"
        cur.execute(select)
        output = cur.fetchall()
        if output:
            print("Phone number already in use please use another number.")
        else:
            otp = str(random.randint(1000,9999))
            print(otp)
            chances = 3
            for i in range(chances):

                enter_otp = input('Enter OTP: ').strip()
                if (otp == enter_otp):
                    what_to_edit = f'phone = "{new_phone}",'
                    break
                else:
                    chances -= 1
                    print(f'Incorrect OTP, try again. You have {chances} chances left')
            break
    else:
        print("Invalid Phone number.")
print(what_to_edit)

# print('''Welcome to MioKumud...
# Press:-
# 1.Login/Signup
# 2.Products
# ''')
# action = input("Select your action: ").strip()
# if (action == '1'):
#     print('''Press:-
#         1. Phone
#         2. Email
#             ''')
#     signup_by = input('Please enter: ')
#     if (signup_by == '1'):
#         result = login.signup_phone(cur)
#         if result:
#             signup_complete, user_details = result
#             print(user_details)
#     if (signup_by == '2'):
#         result = login.signup_email(cur)
#         if result:
#             signup_complete, user_details = result
#             print(user_details)




