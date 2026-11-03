import os
import secrets

import bcrypt
import mysql.connector
from flask import Flask, redirect, render_template, request, session


def _require_env(name):
    value = os.environ.get(name)
    if value is None or value == "":
        raise RuntimeError("Missing required environment variable: " + name)
    return value


SESSION_SECRET = _require_env("SESSION_SECRET")
MYSQL_HOST = _require_env("MYSQL_HOST")
MYSQL_USER = _require_env("MYSQL_USER")
MYSQL_PASSWORD = _require_env("MYSQL_PASSWORD")
MYSQL_DATABASE = _require_env("MYSQL_DATABASE")

app = Flask(__name__)
app.secret_key = SESSION_SECRET
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_COOKIE_SECURE") == "1"


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )


def _ensure_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def _valid_csrf():
    expected = session.get("csrf_token")
    submitted = request.form.get("csrf_token")
    if not isinstance(expected, str) or not isinstance(submitted, str):
        return False
    if not expected or not submitted:
        return False
    return secrets.compare_digest(expected, submitted)


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": _ensure_csrf_token()}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/user_login", methods=["POST", "GET"])
def user_login():
    if request.method != "POST" or not _valid_csrf():
        return "Invalid request", 400
    email = request.form.get("email") or ""
    password = request.form.get("password") or ""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT `ID`, `PASSWORD` FROM `users` WHERE `EMAIL` = %s",
                (email,),
            )
            users = cursor.fetchall()
            if len(users) > 0:
                stored = users[0][1]
                if isinstance(stored, str):
                    stored_bytes = stored.encode("utf-8")
                else:
                    stored_bytes = stored
                try:
                    password_ok = bcrypt.checkpw(password.encode("utf-8"), stored_bytes)
                except (TypeError, ValueError):
                    password_ok = False
                if password_ok:
                    session["user_id"] = users[0][0]
                    return redirect("/page1")
            return redirect("/login")
        finally:
            cursor.close()
    finally:
        conn.close()


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/adduser", methods=["POST"])
def adduser():
    if not _valid_csrf():
        return "Invalid request", 400
    name = request.form.get("uusername") or ""
    email = request.form.get("uemail") or ""
    password = request.form.get("upassword") or ""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT `ID` FROM `users` WHERE `NAME` = %s OR `EMAIL` = %s",
                (name, email),
            )
            existing = cursor.fetchall()
            if len(existing) == 0:
                password_hash = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )
                cursor.execute(
                    "INSERT INTO `users` (`ID`, `NAME`, `EMAIL`, `PASSWORD`) VALUES (NULL, %s, %s, %s)",
                    (name, email, password_hash.decode("utf-8")),
                )
                conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")


@app.route("/page1")
def page1():
    if "user_id" in session:
        return render_template("page1.html")
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
