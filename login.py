import pymysql
import random
import hashlib
import pandas as pd
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
    if email_id:
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
    else:
        print('Please try with valid Email_id')
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

def add_category(cur):
    cat_name = input('Please enter Category Name: ').title().strip()
    ideal_for = input('Ideal_for: ').title().strip()
    if cat_name == '' or  ideal_for == '':
        print('Please enter valid information')
    else:
        select = f'select category_name from category where category_name = "{cat_name}";'
        cur.execute(select)
        output = cur.fetchall()
        if output:
            print('Category already available, please try with new one')
        else:
            insert = f'insert into category (category_name,slug,ideal_for) values("{cat_name}","www.miokumud.com/{cat_name}/","{ideal_for}");'
            cur.execute(insert)
            conn.commit()
            print('New category added')

def add_product(cur):
    product_name = input('Enter Product Name: ').title().strip()
    price = int(input('Enter price: '))
    cat_name = input('Enter Category Name: ').title().strip()
    select = f'select id from category where category_name = "{cat_name}";'
    cur.execute(select)
    out = cur.fetchall()
    if out:
        cat_id = out[0][0]
    else:
        cat_id = ''
        print('Invalid Category, Please enter correct Category')
    description = input('Please enter product description: ')
    return_product = int(input('Press 1 for return and 0 for no return: '))
    if return_product == 0 or return_product == 1:
        pass
    else:
        print('Please enter valid input')
        return_product = ''
    tags = input('Enter tags: ')
    print(return_product,product_name,price,cat_id,description,tags)
    if product_name == '' or price == '' or cat_id == '' or return_product == '':
        print('Please enter complete information')
    else:
        insert = f'insert into products (product_name,price,category_id,slug,description,date_created,date_updated,returns_available,tags) values("{product_name}",{price},{cat_id},"www.miokumud.com/{cat_name}/{product_name}","{description}",now(),now(),{return_product},"{tags}");'
        cur.execute(insert)
        conn.commit()
        print('New Product added')

def view_products(cur):
    print('''Press:
    0.Back
    1.All Products
    2.By category
    3.By Product''')
    view_by = input('Please enter view by: ')
    if view_by == '1' or view_by == '':
        select = f'select * from products;'
        cur.execute(select)
        all_products = cur.fetchall()
        df = pd.DataFrame(all_products,columns=['id','product_name','price','category_id','slug','description','date_created','date_updated','returns_available','tags'])
        print(f'''all products are following:- 
{df}''')
    elif view_by == '2':
        cat_name = input('Enter Category Name: ').title().strip()
        select = f'''SELECT p.* FROM PRODUCTS AS P 
                    JOIN CATEGORY AS C ON P.CATEGORY_ID = C.ID
                    WHERE C.CATEGORY_NAME = '{cat_name}';'''
        cur.execute(select)
        cat_products = cur.fetchall()
        if cat_products:
            df = pd.DataFrame(cat_products,columns=['id','product_name','price','category_id','slug','description','date_created','date_updated','returns_available','tags'])
            print(f'''all products are following:- 
{df}''')
        else:
            print(f'No Product available for Category {cat_name}')
    elif view_by == '3':
        product_name = input('Enter Product Name: ').title().strip()
        select = f'''SELECT * FROM PRODUCTS WHERE product_name = '{product_name}';'''
        cur.execute(select)
        by_products = cur.fetchall()
        if by_products:
            df = pd.DataFrame(by_products,columns=['id','product_name','price','category_id','slug','description','date_created','date_updated','returns_available','tags'])
            print(f'''all products are following:- 
{df}''')
        else:
            print(f'No Product available for {product_name}')
    else:
        print('Invalid Input')
        