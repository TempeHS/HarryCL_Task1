import sqlite3 as sql
import bcrypt
import diary_management as diary
from flask import jsonify
from flask import send_file, Response
import os
import json

def insertUser(devtag, password):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (devtag,password) VALUES (?,?)",
        (devtag, password),
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

def download_user_data(devtag):
    user_data = diary.download(devtag)
    if isinstance(user_data, Response):
        user_data = user_data.get_json()
    formatted_data = {
        "devtag": devtag,
        "message": "Below is your information you have provided us with:",
        "entries": [{
            "project": entry.get("project"),
            "diary_entry": entry.get("diary_entry"),
            "start_time": entry.get("start_time"),
            "end_time": entry.get("end_time"),
            "time_worked": entry.get("time_worked"),
            "repo": entry.get("repo"),
            "developer_notes": entry.get("developer_notes"),
            "code_additions": entry.get("code_additions")  # Explicitly include code_additions
        } for entry in user_data]
    }
    
    data_file = f'temp_{devtag}_data.json'
    with open(data_file, 'w') as f:
        json.dump(formatted_data, f, indent=4)
    
    try:
        return send_file(
            data_file,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'{devtag}_data.json'
        )
    finally:
        os.remove(data_file)