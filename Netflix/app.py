from flask import Flask, render_template
import sqlite3

app = Flask(__name__);

# FK/PK is a junction table ^^ 
# 
# cursor.execute('''CREATE TABLE Authors 
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

    cursor.execute('''CREATE TABLE IF NOT EXISTS Studio(
                   studio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   studio_name VARCHAR,
                   country VARCHAR
                   )''')
  
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Person(
                   person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name VARCHAR,
                   birth_date DATE,
                   nationality VARCHAR
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Content(
                   content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title VARCHAR,
                   content_type VARCHAR,
                   release_year YEAR,
                   maturity_rating FLOAT,
                   description VARCHAR,
                   duration_mins INTEGER,
                   is_original BOOLEAN,
                   studio_id INTEGER,
                   FOREIGN KEY (studio_id) REFERENCES Studio (studio_id)
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Subscription_Plan (
                   plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   plan_name TEXT,
                   price_monthly INTEGER,
                   max_profiles INTEGER,
                   max_simultaneous_streams INTEGER
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Account(
                   account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   email VARCHAR NOT NULL UNIQUE,
                   password_hash VARCHAR,
                   created_at DATETIME,
                   account_status VARCHAR,
                   country_code VARCHAR,
                   preferred_language VARCHAR,
                   plan_id INTEGER,
                   FOREIGN KEY (plan_id) REFERENCES Subscription_Plan(plan_id)
                   )''')

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Device
                   (device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   device_type TEXT,
                   device_name TEXT,
                   last_active DATE,
                   account_id INTEGER,
                   FOREIGN KEY (account_id) REFERENCES Account (account_id)
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Profile(
                   profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   account_id INTEGER,
                   FOREIGN KEY (account_id) REFERENCES Account(account_id)
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment(
                   payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   amount MONEY,
                   payment_date DATE,
                   payment_method VARCHAR,
                   status BOOLEAN,
                   account_id INTEGER,
                   plan_id INTEGER,
                   FOREIGN KEY (account_id) REFERENCES Account(account_id),
                   FOREIGN KEY (plan_id) REFERENCES Subscription_Plan(plan_id)
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Languages(
                   language_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   language_name VARCHAR,
                   iso_code VARCHAR
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Content_Track(
                   track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   track_type VARCHAR,
                   content_id INTEGER,
                   language_id INTEGER,
                   FOREIGN KEY (content_id) REFERENCES Content(content_id),
                   FOREIGN KEY (language_id) REFERENCES Language(language_id)
                   )''')
    

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Profile(
                   person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name VARCHAR,
                   birth_date DATE,
                   nationality VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Genre(
                   genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   genre_name VARCHAR
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rating(
                    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rating_value VARCHAR,
                    rated_at FLOAT,
                    profile_id INTEGER,
                    content_id INTEGER,
                    FOREIGN KEY (profile_id) REFERENCES Profile(profile_id),
                    FOREIGN KEY (content_id) REFERENCES Content(content_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS My_list(
                   list_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   added_at VARCHAR,
                   profile_id INTEGER,
                   content_id INTEGER,
                   FOREIGN KEY (profile_id) references Profile(profile_id),
                   FOREIGN KEY (content_id) REFERENCES Content(content_id)
                   )
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Watch_history(
                   watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   watched_at VARCHAR,
                   progress_seconds INTEGER,
                   profile_id INTEGER,
                   content_id INTEGER,
                   episode_id INTEGER,
                   FOREIGN KEY (profile_id) REFERENCES profile(profile_id),
                   FOREIGN KEY (content_id) REFERENCES Content(content_id),
                   FOREIGN KEY (episode_id) REFERENCES Episode(episode_id)
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Season (
                   season_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   season_number INTEGER,
                   release_year YEAR,
                   content_id INTEGER,
                   FOREIGN KEY (content_id) REFERENCES content(content_id)
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Episode(
                   episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   episode_number INTEGER,
                   title VARCHAR,
                   duration_mins INTEGER,
                   season_id INTEGER,
                   FOREIGN KEY (season_id) REFERENCES Season(season_id)
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Video_Assets(
                   asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   resolution INTEGER,
                   file_url VARCHAR,
                   codec VARCHAR,
                   content_id INTEGER,
                   episode_id INTEGER,
                   FOREIGN KEY (content_id) REFERENCES Content(content_id),
                   FOREIGN KEY (episode_id) REFERENCES Episode(episode_id)
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Content_person(
                   content_id INTEGER,
                   person_id INTEGER,
                   role_type VARCHAR,
                   director VARCHAR,
                   PRIMARY KEY (content_id, person_id),
                   FOREIGN KEY (content_id) REFERENCES Content(content_id),
                   FOREIGN KEY (person_id) REFERENCES Person(person_id)
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Content_genre(
                   content_id INTEGER,
                   person_id INTEGER,
                   genre_id INTEGER,
                   PRIMARY KEY (content_id, person_id),
                   FOREIGN KEY (content_id) REFERENCES Content(content_id),
                   FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
                   )''')

    demo_data = [
        ('jj@gmail.com','iambatman'),
        ('jm@gmail.com', 'eggs are awesome')
    ]

    cursor.executemany("INSERT INTO Account (email, password_hash) VALUES (?,?)", demo_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database Complete :)")