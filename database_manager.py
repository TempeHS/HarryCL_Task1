import sqlite3 as sql
import bcrypt

def insertUser(devtag, password):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (devtag,password) VALUES (?,?)",
        (devtag, password), # no function to encrypt password or exception handling/sanatisaion 
    )
    con.commit()
    con.close()

def userExists(devtag):
    conn = sql.connect('.databaseFiles/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE devtag = ?", (devtag,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def verifyPassword(devtag, password):
    conn = sql.connect('.databaseFiles/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE devtag = ?", (devtag,))
    stored_password = cursor.fetchone()
    conn.close()
    if stored_password:
        return bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8'))
    return False

### example
def getUsers():
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM id7-tusers")
    con.close()
    return cur