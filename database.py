import pymysql
from setting import *

conn = pymysql.connect(host=host, user=user, password=password)
cur = conn.cursor()

# cur.execute(f'''drop database if exists {database}''')
# cur.execute(f'''create database {database}''')
cur.execute(f'''use {database}''')

create_user_table = f'''
        create table if not exists users(
        id int primary key auto_increment,
        name varchar(50),
        username varchar(50) unique,
        password varchar(256) Not Null,
        email varchar(50) unique,
        phone varchar(15) unique,
        date_joined timestamp default current_timestamp Not Null,
        last_login timestamp default current_timestamp Not Null,
        last_access timestamp default current_timestamp Not Null
        );'''
cur.execute(create_user_table)
print("user table created")

create_product_table = f'''
                        create table if not exists products(
                        id int primary key auto_increment,
                        product_name varchar(256) Not Null,
                        price int Not Null,
                        category_id int Not Null,
                        slug varchar(256) unique,
                        description varchar(516),
                        date_created timestamp default current_timestamp Not Null,
                        date_updated timestamp default current_timestamp Not Null,
                        returns_available BIT(1) Not Null,
                        tags varchar(10)
                        )auto_increment=101;'''
cur.execute(create_product_table)
print("product table created")

create_category_table = f'''
                        create table if not exists category(
                        id int primary key auto_increment,
                        category_name varchar(64),
                        slug varchar(512),
                        ideal_for varchar(10)
                        )auto_increment=001;'''
cur.execute(create_category_table)
print("category table created")



