import sys
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
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

def level(Pass):
    password = Pass
    level = 0
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
    if len(password) >= 8:
        level += 1
    if any(i.islower() for i in password):
        level += 1
    if any(i.isupper() for i in password):
        level += 1
    if any(i.isnumeric() for i in password):
        level += 1
    if any(i in special_characters for i in password):
        level += 1

    return level


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
    Welcome to Securify, crafted by the trio of Abhishek Agnal, Darshan Bhandari and Puneeth Nettem. 
    Our passion for security led us to develop this cutting-edge password manager that prioritizes your 
    data's safety.Securify employs a sophisticated encryption system that adapts its decryption technique 
    according to your user-defined key.This dynamic approach adds an extra layer of protection, 
    ensuring that your sensitive information remains secure in an ever-evolving digital landscape.
    What sets Securify apart is its unique ability to support multiple users, providing a tailored and secure 
    experience for each individual.
    Trust Secure7 to be your guardian in the realm of passwords, where innovation meets security.

COMMANDS       
    key: change the decryption key
         - use this in case your passwords doesn't make any sense
    new: Create a new record for your password.
    pass: Retrieve a password using the specified tag.
    show: Display all stored usernames.
    delete: Delete a stored password using the specified tag.
    strength: Assess the strength of stored passwords with a bar graph.
    exit: Close the Securify application.
        """)


    elif command == "new":
        u_name = input("Enter username: ")
        password_raw = input("Enter password: ")
        note = input("Enter note: ")
        tag = input("enter a unique tag to identify your password: ")
        password = encrypt(password_raw, key)
        level = level()
        db.execute(f"INSERT INTO passwords (username, password, note, tag, level) VALUES ('{u_name}', '{password}', '{note}', '{tag}')")
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
        check = db.execute(f"SELECT username,level FROM passwords")
        output = db.fetchall()
        categories = []
        values = []
        for i in range(0, check):
            categories.append(output[i][0])
            values.append(output[i][1])

        plt.bar(categories, values, color='blue')

        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.title('strength')
        plt.show()
    elif command == "":
        continue
    else:
        print("invalid input. try \"help\" for more information")
