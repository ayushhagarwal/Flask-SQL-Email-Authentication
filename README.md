## Flask-SQL-Email-Authentication
A Flask, SQL email authentication web application. The database used for storing user details is MySQL

### Steps To Run the Project

To set up the database you can create an account on https://remotemysql.com. Create a databse there, it will give you an username and password to the database. Note that down. 
Connect to that database using the below syntax. Just replace the username, password,databse name on the code.
```
conn=mysql.connector.connect(host="remotemysql.com",user="",password="",database="")
```

Now open that database in "myphpadmin" using the same credentials and create a table in it. 
The configuration of the table should be as followed:
* Table name= "users"
Add four columns: 
1. ID (datatype INT)
2. NAME (VARCHAR 64 characters)
3. EMAIL (VARCHAR 64 characters)
4. PASSWORD (VARCHAR 128 characters)

Another way to setup the databse is doing it locally. Everything remains same just you do all the above stuff on local and make minor changes on code to connect. Instead of database name create a new schema and use that name there.
This is the changes you should do: 
```
conn=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="your databse name",auth_plugin='mysql_native_password')
```

That is it. Next install the flask dependencies referring the requirements.txt file and type "python app.py" in the terminal. 

For any further queries you can mail me or connect with me on twitter (@_ayushagarwal11)
