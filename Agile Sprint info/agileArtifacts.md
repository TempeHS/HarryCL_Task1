# List of achievables

---

- Developer Log entries are time/date stamped
- Develop a database from a schema which includes feild names, primary and foreign keys and joins
- Summary of diary entries are rendered to the home page
- Input sanitisation for all diary inputs

# Increment (what must achieved by end of sprint)

---

- Users can create entries
- Entries are timestamped, and linked to developer name
- Entry inputs are sanatised
- Entries are rendered to the home page

# Sprint Review (focus on project management)

---

## What challenges did you have

- Configuring the routes the user will from login -> 2FA -> home page whilst keeping session data
- Getting the API to render summarised diary entries to the home page
- Attempted to create search and filter but failed
- Abstracting main.py code into functions in other files

## What did you do well

- Implemented the route from the entry form -> API -> database efficently
- Created a logs.html partial so I can use it on my search page when needed
- Improved upon session mangement
- Created a database with foreign key and join

## What will you do differently next time

- Do more research on flask search using mainly the API
- Trust my own intuition
