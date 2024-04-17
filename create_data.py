#! /usr/bin/env python3

import json, random, string
from hashlib import sha3_512
from mysql.connector import connect, Error
from colorama import Fore

database = "sharn_student_cloud"
NEWLINE = '\n'
password_characers = string.ascii_letters

with open("db_user.json", 'r') as file:
    login_details = json.load(file)
with open("data.json", 'r') as file:
    data = json.load(file)
with open("user.json") as file:
    users = json.load(file)

def createEntity(entity):
    return f'("{entity["roll"]}", "{entity["name"]}", "{entity["gender"]}", "{entity["department"]}", "{entity["programme"]}", "{entity["roomNumber"]}", "{entity["hostel"]}", "{entity["bloodgroup"]}", "{entity["city"]}"),'
def createUser(user):
    return f'("{user}", "{sha3_512(user.encode()).hexdigest()}", "{generatePassword(40)}"),'
def generatePassword(length):
    return ''.join([random.choice(password_characers) for _ in range(length)])

if __name__ == "__main__":
    try:
        with connect(
            host="localhost",
            user=login_details["user"],
            password=login_details["password"],
        ) as connection:
            print("Connected to MySQL Successfully!")
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {database}")
                print(f"Created Database {Fore.GREEN}{database}{Fore.RESET}")
                cursor.execute(f"USE {database}")
                cursor.execute(f"""CREATE TABLE STUDENTS(
                               roll VARCHAR(20) PRIMARY KEY,
                               name VARCHAR(100),
                               gender VARCHAR(6),
                               department VARCHAR(50),
                               programme VARCHAR(20),
                               roomNumber VARCHAR(10),
                               hostel VARCHAR(10),
                               bloodgroup VARCHAR(20),
                               city VARCHAR(100)
                )""")
                print(f"Created Table {Fore.CYAN}STUDENTS{Fore.RESET}")
                cursor.execute(f"""INSERT INTO STUDENTS ({', '.join(data[0].keys())}) VALUES
{NEWLINE.join([createEntity(student) for student in data])}
("2626", "Kaptaan", "Male", "Mechanical Engineering", "BTech", "", "", "O+", "Ropar, Panjab")
                """)
                print(f"Inserted  Data of {Fore.BLUE}{len(data)}{Fore.RESET} Students")
                cursor.execute(f"""CREATE TABLE USERS(
                               user VARCHAR(20) PRIMARY KEY,
                               userhash VARCHAR(128),
                               password VARCHAR(40)
                )""")
                print(f"Created Table {Fore.CYAN}USERS{Fore.RESET}")
                cursor.execute(f"""INSERT INTO USERS (user, userhash, password) VALUES
{NEWLINE.join([createUser(user) for user in users])}
("kaptaan", "{sha3_512('kaptaan'.encode()).hexdigest()}", "Totally_Unbreakable_Password")
                """)
                print(f"Inserted  Data of {Fore.BLUE}{len(users)}{Fore.RESET} Users")
                connection.commit()
    except Error as err:
        print(err)