import bleach
from datetime import datetime
import logging

def entry_input(session, request_form):
    devtag = session.get("devtag")
    project = request_form["project"]
    project = bleach.clean(project)
    diary_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = datetime.strptime(request_form["start_time"], "%Y-%m-%dT%H:%M")
    end_time = datetime.strptime(request_form["end_time"], "%Y-%m-%dT%H:%M")
    time_diff = (end_time - start_time).total_seconds() / 60
    time_worked = round(time_diff / 60 * 4) / 4 
    repo = request_form["repo"]
    developer_notes = request_form["developer_notes"]
    developer_notes = bleach.clean(developer_notes)
    code_additions = request_form["code_additions"]
    code_additions = bleach.clean(code_additions)
    
    data = {
        "devtag": devtag,
        "project": project,
        "diary_entry": diary_entry,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),  
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),      
        "time_worked": str(time_worked),
        "repo": repo,
        "developer_notes": developer_notes,
        "code_additions": code_additions,
    }
    
    return data
