from flask import jsonify
import sqlite3 as sql
from jsonschema import validate
from flask import current_app
from datetime import datetime
import logging

schema = {
    "type": "object",
    "validationLevel": "strict",
    "required": [
        "devtag",
        "project",
        "start_time",
        "end_time",
        "time_worked",
        "repo",
        "developer_notes",
        "code_additions",
        "diary_entry",
    ],
    
    "properties": {
        "devtag": {"type": "string"},
        "project": {"type": "string"},
        "start_time": {"type": "string"},
        "end_time": {"type": "string"},
        "diary_entry": {"type": "string"},
        "time_worked": {"type": "string"},
        "repo": {"type": "string"},
        "developer_notes": {"type": "string"},
        "code_additions": {"type": "string"},
    },
}


def diary_add(entry):
    if validate_json(entry):
        con = sql.connect(".databaseFiles/database.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO diary_entries (devtag, project, start_time, end_time, diary_entry, time_worked, repo, developer_notes, code_additions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            [
                entry["devtag"],
                entry["project"],
                entry["start_time"],
                entry["end_time"],
                entry["diary_entry"],
                entry["time_worked"],
                entry["repo"],
                entry["developer_notes"],
                entry["code_additions"],
            ],
        )
        con.commit()
        con.close()
        return {"message": "Extension added successfully"}, 201
    else:
        return {"error": "Invalid JSON"}, 400

def diary_get():
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM diary_entries")
    migrate_data = [
        dict(
            id=row[0],
            devtag=row[1],
            project=row[2],
            start_time=row[3],
            end_time=row[4],
            time_worked=row[5],
            repo=row[6],
            developer_notes=row[7],
            code_additions=row[8],
            diary_entry=row[9],
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)

def get_entry(entry_id):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM diary_entries WHERE id=?", [entry_id])
    row = cur.fetchone()
    con.close()
    if row:
        entry = {
            "id": row[0],
            "devtag": row[1],
            "project": row[2],
            "start_time": row[3],
            "end_time": row[4],
            "time_worked": row[5],
            "repo": row[6],
            "developer_notes": row[7],
            "code_additions": row[8],
            "diary_entry": row[9],
        }
        return jsonify(entry)
    else:
        return jsonify({"error": "Entry not found"}), 404

def diary_search(filters=None):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    query = "SELECT * FROM diary_entries"
    params = []
    if filters:
        conditions = []
        if "devtag" in filters and filters["devtag"]:
            conditions.append("devtag LIKE ?")
            params.append(f"%{filters['devtag']}%")
        if "project" in filters and filters["project"]:
            conditions.append("project LIKE ?")
            params.append(f"%{filters['project']}%")
        if "repo" in filters and filters["repo"]:
            conditions.append("repo LIKE ?")
            params.append(f"%{filters['repo']}%")
        if "diary_entry" in filters and filters["diary_entry"]:
            conditions.append("diary_entry LIKE ?")
            params.append(f"%{filters['diary_entry']}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    logging.debug(f"Executing query: {query} with params: {params}")
    cur.execute(query, params)
    rows = cur.fetchall()
    con.close()
    migrate_data = [
        dict(
            id=row[0],
            devtag=row[1],
            project=row[2],
            start_time=row[3],
            end_time=row[4],
            time_worked= row[5],
            repo=row[6],
            developer_notes=row[7],
            code_additions=row[8],
            diary_entry=row[9],
        )
        for row in rows
    ]
    return jsonify(migrate_data)

def download(devtag):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM diary_entries WHERE devtag=?", [devtag])
    rows = cur.fetchall()
    con.close()
    migrate_data = [
        dict(
            id=row[0],
            devtag=row[1],
            project=row[2],
            start_time=row[3],
            end_time=row[4],
            time_worked=row[5],
            repo=row[6],
            developer_notes=row[7],
            code_additions=row[8],
            diary_entry=row[9],
        )
        for row in rows
    ]
    return jsonify(migrate_data)

def delete_user(devtag):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM diary_entries WHERE devtag=?", [devtag])
    cur.execute("DELETE FROM users WHERE devtag=?", [devtag])
    con.commit()
    con.close()
    return {"message": "User and Data deleted successfully"}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False