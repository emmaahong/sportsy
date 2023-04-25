DROP TABLE IF EXISTS posts;

CREATE TABLE [IF NOT EXISTS] schema.users (
    usernumber INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    passcode TEXT NOT NULL
);

