-- database: database.db
CREATE TABLE users(id INTEGER PRIMARY KEY autoincrement,devtag TEXT NOT NULL UNIQUE, password TEXT NOT NULL);

-- INSERT INTO id7-tusers(username,password) VALUES ("","");

-- SELECT * FROM extension;

CREATE TABLE diary_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devtag TEXT NOT NULL,
    project TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    time_worked TEXT NOT NULL,
    repo TEXT NOT NULL,
    developer_notes TEXT NOT NULL,
    code_additions TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (devtag) REFERENCES users (devtag)
);

CREATE TABLE diary_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devtag TEXT NOT NULL,
    project TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    time_worked TEXT NOT NULL,
    repo TEXT NOT NULL,
    developer_notes TEXT NOT NULL,
    code_additions TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (devtag) REFERENCES users (devtag)
);

DROP TABLE IF EXISTS diary_entries;