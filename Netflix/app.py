from flask import Flask, render_template
import sqlite3

app = Flask(__name__);

# FK/PK is a junction table ^^ cursor.execute('''CREATE TABLE Authors 
 #                  (author_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
   # cursor.execute('''CREATE TABLE Books 
 #                  (book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)''')
  #  cursor.execute(''' CREATE TABLE Book_Authors
   #                (book_id INTEGER, author_id INTEGER, 
     #              FOREIGN KEY (book_id) REFERENCES Books (book_id), 
      #             FOREIGN KEY (author_id) REFERENCES Authors (author_id))''')

def init_db():
    conn = sqlite3.connect('library_system.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''CREATE TABLE IF NOT EXISTS Account
                   (account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY (plan_id) REFERENCES Subscription_Plan (plan_id),
                   email VARCHAR NOT NULL UNIQUE,
                   password_hash VARCHAR,
                   created_at, DATETIME,
                   account_status TEXT,
                   country_code INTEGER,
                   preferred_language TEXT)''')
    
    email = [
        ('jaydenmurillo325@gmail.com',),
        ('jaydenmurillo524@gmail.com',)
    ]

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Device
                   (device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY account_id REFERENCES Account (account_id),
                   device_type TEXT,
                   device_name TEXT,
                   last_active DATE
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Subscription_plan (
                   plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   plan_name TEXT,
                   price_monthly INTEGER,
                   max_profiles INTEGER,
                   max_simultaneous_streams INTEGER
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Profile(
                   profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY account_id REFERENCES Account(account_id),
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment(
                   payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY account_id REFERENCES Account(account_id),
                   FOREIGN KEY plan_id REFERENCES Subscription_plan(plan_id),
                   amount MONEY,
                   payment_date DATE,
                   payment_method VARCHAR,
                   status BOOLEAN
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  Languages(
                   language_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   language_name VARCHAR,
                   iso_code VARCHAR
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS  Content_Track(
                   track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY content_id REFERENCES Content(content_id),
                   FOREIGN KEY language_id REFERENCES Language(language_id),
                   track_type VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  Content(
                   content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FOREIGN KEY studio_id REFERENCES Studio(studio_id),
                   title VARCHAR,
                   content_type VARCHAR,
                   release_year YEAR,
                   maturity_rating FLOAT,
                   description VARCHAR,
                   duration_mins INTEGER,
                   is_original BOOLEAN
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS  Studio(
                   studio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   studio_name VARCHAR,
                   country VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  Profile(
                   person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name VARCHAR,
                   birth_date DATE,
                   nationality VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  Genre(
                   genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   genre_name VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  Rating(
                    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    FOREIGN KEY profile_id REFERENCES Profile(profile_id),
                    FOREIGN KEY content_id REFERENCES Content(content_id),
                    rating_value VARCHAR,
                    rated_at FLOAT
                    )''')


    




    cursor.execute('''CREATE TABLE IF NOT EXISTS  ''')



    conn.commit()
    conn.close()
    