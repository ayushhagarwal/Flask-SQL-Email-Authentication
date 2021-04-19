from flask import Flask, render_template, url_for,request,redirect,session
from flask import Response
import mysql.connector
import ssl
import os,bcrypt




app=Flask(__name__)
app.secret_key=os.urandom(24)
salt=b'$2b$12$Kh9S5S4FHT.WhzBa8tLZvO'



cursor=conn.cursor()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user_login",methods=['POST','GET'])
def user_login():
    email=request.form.get('email')
    password=request.form.get('password')
    password=bcrypt.hashpw(password.encode('utf-8'),salt)
    cursor.execute("""SELECT * FROM `users` WHERE `EMAIL` LIKE '{}' AND `PASSWORD` LIKE "{}" """.format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return "login successful"
    else:
        return redirect('/login')


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/adduser", methods=['POST'])
def adduser():
    name=request.form.get('uusername')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    password=bcrypt.hashpw(password.encode('utf-8'),salt)
    # print(salt)
    print(password)
    cursor.execute("""SELECT * FROM `users` WHERE `EMAIL` LIKE '{}' """.format(email))
    user=cursor.fetchall()
    if len(user)>0:
        return "email id already exists, please try with another one"
    else:
        cursor.execute("""INSERT INTO `users` (`ID`,`NAME`,`EMAIL`,`PASSWORD`) VALUES 
        (NULL,'{}','{}',"{}")""".format(name,email,password))
    conn.commit()
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

    
if __name__=="__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True)     