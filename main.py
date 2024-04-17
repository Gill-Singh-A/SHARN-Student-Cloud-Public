#! /usr/bin/env python3

import json
from hashlib import sha3_512
from flask import Flask, render_template, request
from mysql.connector import connect, Error

app = Flask(__name__)
host = "127.0.0.1"
port = 7829
debug = True
database = "sharn_student_cloud"
flag = "pclub{d!d_Y0u_try_$q1i_0n_10gin_xdxd}"

student_fields = ['roll', 'name', 'gender', 'department', 'programme', 'roomNumber', 'hostel', 'bloodgroup', 'city']

with open("db_user.json", 'r') as file:
    login_details = json.load(file)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        connection = connect(host="localhost", user=login_details["user"], password=login_details["password"])
        cursor = connection.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute(f"SELECT password FROM USERS WHERE userhash='{sha3_512(user.encode()).hexdigest()}'")
        original_password = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(original_password) == 1:
            original_password = original_password[0][0]
            if original_password == password:
                if user == "kaptaan":
                    return render_template("file.html", message=flag)
                else:
                    return render_template("file.html", message="User have not File or Data to Show!")
            else:
                return render_template("login.html", message="Incorrect Password")
        else:
            return render_template("login.html", message="User Not Found")
    return render_template("login.html")
@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")
@app.route("/recovery", methods=["GET"])
def recovery():
    return render_template("recovery.html")
@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")
@app.route("/searchRoll", methods=["POST"])
def searchRoll():
    roll = request.json["roll"]
    connection = connect(host="localhost", user=login_details["user"], password=login_details["password"])
    cursor = connection.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"SELECT * FROM STUDENTS WHERE roll='{roll}'")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(result) > 0:
        result = result[0]
        return {key: result[index] for index, key in enumerate(student_fields)}
    else:
        return {}

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)