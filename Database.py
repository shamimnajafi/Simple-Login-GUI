import sqlite3
conn = sqlite3.connect("MyDatabase.db")
cur = conn.cursor()
query = """
    CREATE TABLE IF NOT EXISTS login_info(
    username VARCHAR,
    password VARCHAR,
    name VARCHAR,
    lastname VARCHAR,
    age INTEGER,
    gender VARCHAR,
    nationality VARCHAR,
    education VARCHAR    
    );
 """
cur.execute(query)
conn.commit()
conn.close()





