# Import the sqlite3 module
import sqlite3
from sqlite3 import Error

import getpass

#-- global variables
retry=False
name="Mydatabase.db"
username="Martica"
email="bho@hotmail.it"
email2="bho2@hotmail.it"
password="password"


# Setup a connection with our database file
with sqlite3.connect("Mydatabase.db") as db:
  pass

#Or create connectionf functions with exception handling
def create_connection(db_file):
#create a database connection to a SQLite database 
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()





#Create table Members into a database
def create_table(databasename):
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  sql='CREATE TABLE IF NOT EXIST Members("member_ID" INTEGER PRIMARY KEY AUTOINCREMENT,username text, email text, password text)'
  result=curs.execute(sql)
  if not result:
    print("It isn't in database")
  else:
    print("It is in database")
  conn.commit()
  conn.close()


#Display table Members
def display_database(databasename):
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  curs.execute('SELECT * FROM Members')
  print(curs.fetchall())
  conn.close()


#Add to database
def add_to_database(databasename,username,email,password):
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  #I took off member_ID and '%d'
  curs.execute("INSERT INTO Members(\
  username, email, password) \
   VALUES ('%s', '%s', '%s' )" % \
   ( username, email,password))
  conn.commit()
  curs.execute('SELECT * FROM Members')
  print(curs.fetchall())
  conn.close()


#Drop table
def drop_table(databasename):
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  curs.execute("DROP TABLE IF EXISTS Members")
  print("Table deleted")
  conn.close()


#Remove rows from database
#Adjust query
def remove_data(name):
  conn = sqlite3.connect(name)
  curs = conn.cursor()
  Item_to_delete = input("please enter the item you wish to delete")
  sql = "  DELETE FROM Members  WHERE Name = '{0}' ".format(Item_to_delete) #{0} means item 1 in formatting
  curs.execute(sql)   #Where to delete, replace Dave with item name to delete
  conn.commit()
  conn.close()


#Update database email
#Adjust query
def update(databasename,email,username):
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  sql = "UPDATE Members \
  SET email = '%s'  WHERE \
  username = '%s'"%(email,username)
  curs.execute(sql) 
  conn.commit()
  conn.close()


#Check if username is in db
def check_usernamedb(databasename,username):
  global retry
  conn = sqlite3.connect(databasename)
  curs = conn.cursor()
  sql="SELECT member_ID,username FROM Members \
  WHERE \
  username = '%s'"%(username)
  curs.execute(sql)
  #Length array, if it's zero username is not in db
  result=len(curs.fetchall())
  if result==0:
    print("Username not in database please register")
    retry=True
  else:
    retry=False
  conn.commit()
  conn.close()
  return retry


  #Check if password is right for the given username
  #This function checks the match between username and password if the user exists
def check_password(databasename,username,password):
  global retry
  conn=sqlite3.connect(databasename)
  curs=conn.cursor()
  sql="SELECT username,password FROM Members \
  WHERE username= '%s' \
  and password= '%s'"%(username,password)
  curs.execute(sql)
  #Length array, password is in db?
  result=len(curs.fetchall())
 # if result=0 password doesn't match with username
  if result==0:
    print("Password doesn't match with username")
    retry=True
  else:
    retry=False
  conn.commit()
  conn.close()
  return retry



  #Check if e-mail is in db

def check_email(databasename,email):
  global retry
  conn=sqlite3.connect(databasename)
  curs=conn.cursor()
  sql="SELECT username, email FROM Members\
  WHERE email='%s'"%(email)
  curs.execute(sql)
  result=len(curs.fetchall())
  #Length array to check if email is already in db
  if result!=0:
    print("User already registered with this e-mail")
    retry=True
  else:
    retry=False
  conn.commit()
  conn.close()
  return retry






#Functions for Login System 

#Log In or Register?
def question():
  global question
  global answer
  question=print("Log In. Are you already a member??")
  answer=input("Yes or No? ")
  return answer



#Credentials or subscribe
def credentials(answer):
  global retry
  global name,password
  if answer=='Yes': 
    print("Insert username and password:")
    #Insert username
    username = input("username: ")
    #Check if username is empty
    validate_username(username)
    #Check if username is in db
    retry= check_usernamedb(name,username)
    if retry==False:
      password=insert_password()
      #is password empty?
      validate_password(password)
      #Check if password is right
      retry=check_password(name,username,password)
  elif answer=='No':
    #Register usign the e-mail
    email=email_subscribe()
    #Check if e-mail is valid
    validate_email(email)
    #Check if e-mail is in db
    check_email(name,email)
    #Insert username
    username=insert_new_username(name)
    #Check if e-mail is in db
    retry1=check_usernamedb(name,username)
    retry=not retry1
    if retry==True:
      print("Username already used, put another one ")
      retry=True
    else:
      print("Insert 2 passwords:")
      #insert 2 passwords to confirm
      password=insert_new_psw(name)
    #add these informations to db
    add_to_database(name,username,email,password)
    #print(retry)
    #display_database(name)
  else:
    print("Invalid answer. Try again")
    retry=True
  return retry



#Register usign the e-mail
def email_subscribe():
  global password
  print("Insert e-mail:")
  #Insert e-mail
  email=input("email: ")
  return email



#check length and if  email are valid
def validate_email(eml):
  while not eml or "@" not in eml:
    print("E-mail not valid!")
    eml=input("Insert e-mail again: ")
     #empty before @?
    counter=eml.find("@")
    while counter==-1 or counter==0:
      #if counter== or counter==-1:
      print("E-mail not valid!")
      eml=input("Insert e-mail again: ")
    #check on domain and e-mail length
    domain=eml[counter:]
    while len(domain)>64 and len(eml)>254:
      print("E-mail not valid!")
  return 


#Register with new username:

def insert_new_username(databasename):
  #Insert username
  username = input("username: ")
  #Check if username is valid
  validate_username(username)
  return username



#Insert new passwords
def insert_new_psw(databasename):
  #Insert password1
  password1=input("password1: ")
  #Check if it is empty
  validate_password(password1)
  #Insert password2
  password2=input("Insert again password to confirm: ")
  #Check if they are equal
  confirm_inserted_psw(password1,password2)
  retry=False
  return password2



#Insert Password
def insert_password():
  password=input("Enter your password: ")
  #getpass.getpass("Enter your password: ")
  return password



#Check username isn't empty
def validate_username(user):
  while not user:
     print("Username empty")
     user=input("Insert username again: ")
  return


#Check password isn't empty
def validate_password(psw):
  while not psw:
    print("Password empty")
    psw=input("Enter your password: ")
  return


#Password1==Password2?
def confirm_inserted_psw(psw1,psw2):
  while psw1!=psw2:
    print("Password1 isn't equal to password1. Try again!")
    psw2=input("password2: ")
  return












#Start Login
def start_login():
  answer=question()
  ahead= credentials(answer)
  return ahead

#To define:





#Password1==Password2?

#store info in Database

#check legth and validity of password

#retry for validate_*() functions







#create_table(name)
#update(name,email2,username)
#display_database(name)
#add_to_database(name,username,email,password)
#drop_table(name)


#Start program for Login System
#display_database(name)
ahead= start_login()
while ahead:
  print("Log In. Are you already a member??")
  answer=input("Yes or No? ")
  ahead= credentials(answer)

