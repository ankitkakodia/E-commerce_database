import pymysql
import random
import hashlib
from database import cur,conn


def signup_phone(cur):
    phone = input('Enter Phone Number:').strip()
    if (len(phone) != 10):
        print('Please try with valid Phone Number')
    else:
        otp = str(random.randint(1000,9999))
        print(otp)
        #sent to phone
        chances = 3
        for i in range(chances):
            enter_otp = input('Enter OTP: ').strip()
            if (otp == enter_otp):
                select = f'select phone from users where phone = "{phone}";'
                cur.execute(select)
                user_details = cur.fetchall()
                if user_details:
                    update = f'update users set last_login = now(),last_access = now() where phone = {phone};'
                    cur.execute(update)
                    conn.commit()
                    print('Login Successfully')
                    return(True,phone)
                else:
                    insert = f'insert into users(phone) values("{phone}");'
                    cur.execute(insert)
                    conn.commit()
                    print('Signup Successfully')
                    return(True,phone)
                #break
            else:
                chances -= 1
                print(f'Incorrect OTP, try again. You have {chances} chances left')


def signup_email(cur):
    email_id = input("Email_id: ").strip()
    select = f"select email, password from users where email = '{email_id}';"
    cur.execute(select)
    user_details = cur.fetchall()
    if user_details:
        password = input("Please enter password to login: ").strip()
        password = hashlib.sha256(password.encode())
        password = password.hexdigest()
        if (password == user_details[0][1]):
            update = f'update users set last_login = now(),last_access = now() where email = "{email_id}";'
            cur.execute(update)
            conn.commit()
            print('Login Successfully')
            return(True,user_details)
        else:
            print('Please enter correct password')  
    else:
        password = input("Please enter password to Signup: ").strip()
        password = hashlib.sha256(password.encode())
        password = password.hexdigest()
        otp = str(random.randint(1000,9999))
        print(otp)
        chances = 3
        for i in range(chances):
            enter_otp = input('Enter OTP: ').strip()
            if (otp == enter_otp):
                insert = f'insert into users(email,password) values("{email_id}","{password}");'
                cur.execute(insert)
                conn.commit()
                print('Signup Successfully')
                return(True,user_details)
            else:
                chances -= 1
                print(f'Incorrect OTP, try again. You have {chances} chances left')

def profile_edit(cur,user_details):
    if len(user_details[0])>1:
        what_to_edit = ''
        full_name = input("Please enter Full name: ").title().strip()
        if not full_name == '':
            what_to_edit += f'name = "{full_name}",'
        new_password = input("Choose password: ").strip()
        if not new_password == '':
            new_password = hashlib.sha256(new_password.encode())
            new_password = new_password.hexdigest()
            what_to_edit += f'password = "{new_password}",'
        while True:
            new_phone = input("Please enter phone").strip()
            if (len(new_phone)== 10):
                select = f"select phone from users where phone = '{new_phone}';"
                cur.execute(select)
                output = cur.fetchall()
                if output:
                    print("Phone number already in use please use another number.")
                else:
                    otp = str(random.randint(1000,9999))
                    chances = 3
                    for i in range(chances):
                        enter_otp = input('Enter OTP: ').strip()
                        if (otp == enter_otp):
                            what_to_edit += f'phone = "{new_phone}",'
                        else:
                            chances -= 1
                            print(f'Incorrect OTP, try again. You have {chances} chances left')
                    break
            else:
                print("Invalid Phone number.")


        
    else:
        print('phone')





# def signup(cur):
#     first_name = input("Please enter First name: ")
#     last_name = input("Please enter Last name: ")
#     username = input("Choose username: ")
#     password = input("Choose password: ")
#     email = input("Please enter")
#     select = f"select username from users where username = '{username}';"
#     cur.execute(select)
#     usernames = cur.fetchall()
    
#     if (len(usernames)==0):
#         insert = f"insert into users (first_name,last_name,password,username) values('{first_name}','{last_name}','{password}','{username}');"
#         cur.execute(insert)
#         print("Signup Successfully")
#         return True, username
#     else :
#         print("Username Already exists, please try again!!!")')

# def login(cur):
#     username = input("Username: ")
#     password = input("Password: ")
#     select = f"select username, password from users where username = '{username}' and password = '{password}';"
#     cur.execute(select)
#     user_details = cur.fetchall()
    
#     if (len(user_details) == 0):
#         print("Wrong Username/password or Please signup first!!")
#     else :
#         print("Login Successfully!!!")
#         return True, user_details
            

