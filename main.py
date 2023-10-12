import sys
import pymysql
import pandas as pd
from colorama import Fore, Back, Style, init


connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', database="project", password='Abhi@mysql#0168',
                             charset='utf8')

db = connection.cursor()


def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        encrypted_text += chr((ord(char) + key) % 0x110000)
    return encrypted_text


def decrypt(encrypted_text, key):
    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += chr((ord(char) - key) % 0x110000)
    return decrypted_text

global key
passwd = input(f"{Style.DIM}enter decryption key:{Style.RESET_ALL} ")
for i in passwd:
    if i.isnumeric():
        key = int(passwd)
    else:
        print (f"{Fore.RED}Error{Style.RESET_ALL}: password must be numeric")
        db.close()
        sys.exit()

while True:
    command = input(f"\n[superuser@{Fore.GREEN}{key}{Style.RESET_ALL}]$ ")
    if command == "exit":
        db.close()
        break
    elif command == "help":
        print ("""
ABOUT
    Welcome to Secure7, crafted by the trio of Abhishek Agnal, Darshan Bhandari and Punith Nettam. 
    Our passion for security led us to develop this cutting-edge password manager that prioritizes your 
    data's safety.Secure7 employs a sophisticated encryption system that adapts its decryption technique 
    according to your user-defined key.This dynamic approach adds an extra layer of protection, 
    ensuring that your sensitive information remains secure in an ever-evolving digital landscape. 
    Trust Secure7 to be your guardian in the realm of passwords, where innovation meets security.

COMMANDS       
    key: change the decryption key
         - use this in case your passwords doesn't make any sense
    new: store a new password
    pass: retrive password using the unique tag specified while creating a new record
    show: show all stored usernames
    delete: delete stored passwords using the unique tag specified while creating a new record
    strength: bar graph of strength of the passwords stored
    exit: exit the application
        """)


    elif command == "new":
        u_name = input("Enter username: ")
        password_raw = input("Enter password: ")
        note = input("Enter note: ")
        tag = input("enter a unique tag to identify your password: ")
        password = encrypt(password_raw, key)
        db.execute(f"INSERT INTO passwords (username, password, note, tag) VALUES ('{u_name}', '{password}', '{note}', '{tag}');")
        connection.commit()
        print ("record added successfully")
        print (f"{Fore.YELLOW}warning{Style.RESET_ALL}: Dont forget the key in use at the time of creating new password")


    elif command == "key":
        passwd = input(f"{Style.DIM}enter new decryption key:{Style.RESET_ALL} ")
        for i in passwd:
            if i.isnumeric():
                key = int(passwd)
            else:
                print (f"{Fore.RED}Error{Style.RESET_ALL}: password must be numeric")
    elif command == "pass":
        tag = input("enter tag: ")
        check = db.execute(f"SELECT * FROM passwords WHERE tag = '{tag}'")
        if check != 0:
            output = db.fetchall()[0]
            print ("password: ", decrypt(output[2], key))
        else:
            print ("no records found")


    elif command == "delete":
        tag = input("enter tag: ")
        check = db.execute(f"DELETE FROM passwords WHERE tag = '{tag}'")
        if check != 0:
            print ("record deleted successfully.")
        else:
            print ("no records found")
        connection.commit()


    elif command == "show":
        check = db.execute(f"SELECT username, tag FROM passwords")
        output = db.fetchall()
        if check != 0:
            NAME = []
            TAG = []
            for a, b in output:
                NAME.append(a)
                TAG.append(b)
            data = {
                "Username": NAME,
                "Tag": TAG
            }
            df = pd.DataFrame(data)

            print (df.to_string(index=False))

            df = pd.DataFrame(data)

        else:
            print ("no records found")

    elif command == "strength":
        print ("Hey, password pioneers! Our coding maestros are crafting a wizardly update—soon, your passwords will reveal their strength secrets. Prepare for the magic, unfolding soon on our GitHub stage")

    elif command == "":
        continue
    else:
        print("invalid input. try \"help\" for more information")
