from flask import jsonify
import sqlite3 as sql
from jsonschema import validate
from flask import current_app

schema = {
    "type": "object",
    "validationLevel": "strict",
    "required": [
        "developer",
        "project",
        "start_time",
        "end_time",
        "diary_entry",
        "time_worked",
        "repo",
        "developer_notes",
        "code_additions",
    ],
    
    "properties": {
        "developer": {"type": "string"},
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

def diary_get():
    con = sql.connect(".database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM diary_entries")
    migrate_data = [
        dict(
            developer=row[0],
            project=row[1],
            start_time=row[2],
            end_time=row[3],
            diary_entry=row[4],
            time_worked=row[5],
            repo=row[6],
            developer_notes=row[7],
            code_additions=row[8],
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)

def diary_add(entry):
    if validate_json(entry):
        con = sql.connect(".database/data_source.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO diary_entries (developer, project, start_time, end_time, diary_entry, time_worked, repo, developer_notes, code_additions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            [
                entry["developer"],
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

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False