## Flask-SQL-Email-Authentication
A Flask, SQL email authentication web application. The database used for storing user details is MySQL

### Steps To Run the Project

To set up the database you can create an account on https://remotemysql.com. Create a databse there, it will give you an username and password to the database. Note that down. 
Connect to that database using the below syntax. Just replace the username, password,databse name on the code.

Replace the below code snippet on line 14.
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
Run the following command to install all the reuqired dependencies : 
```
pip install -r requirements.txt
```
After installing the dependencies run the project using the following command in terminal: 
```
python app.py
```

##### List of features on the application : 
1. Users can log in only if his credentials are present in database.

2. Without logging in the user cannot go to next page even with using routes of that particular page.

3. When logged in the user can go to other pages using routes.

4. After clicking on logout the user cannot go to next page again using routes.

5. If the email or username already exists in the database the user will not be allowed to create the account.

For any further queries you can mail me or connect with me on twitter (@ayushdev_24)
