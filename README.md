## Flask-SQL-Email-Authentication
A Flask, SQL email authentication web application. The database used for storing user details is MySQL.

### Steps To Run the Project

Create a MySQL database and a `users` table. You can use a local MySQL server or a hosted MySQL database. Do not put real credentials in source files.

The `users` table needs four columns:
1. ID (datatype INT, primary key, auto increment)
2. NAME (VARCHAR 64 characters)
3. EMAIL (VARCHAR 64 characters)
4. PASSWORD (VARCHAR 128 characters) — stores a bcrypt password hash

Set these environment variables before starting the app. Replace the placeholders with your own values. `FLASK_COOKIE_SECURE` should be `1` only when the app is served over HTTPS.

```
export SESSION_SECRET="replace-with-a-long-random-string"
export MYSQL_HOST="127.0.0.1"
export MYSQL_USER="your-mysql-user"
export MYSQL_PASSWORD="your-mysql-password"
export MYSQL_DATABASE="your-database-name"
export FLASK_COOKIE_SECURE="0"
```

The app will not start if `SESSION_SECRET`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, or `MYSQL_DATABASE` is missing.

Install the dependencies and start the app:

```
pip install -r requirements.txt
python app.py
```

The app listens on 127.0.0.1 port 5001.

##### List of features on the application :
1. Users can log in only if his credentials are present in database.

2. Without logging in the user cannot go to next page even with using routes of that particular page.

3. When logged in the user can go to other pages using routes.

4. After clicking on logout the user cannot go to next page again using routes.

5. Signup returns the same page whether or not the name or email is already registered.

For any further queries you can mail me or connect with me on twitter (@ayushdev_24)
