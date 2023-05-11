DROP TABLE IF EXISTS login;

create table login(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fn text not null,
    ln text not null,
    email text not null,
    passcode text not null,
    pb text,
    health_info text not null
);

-- insert into login values(
--     'xyz@gmail.com','XYZ123abc'
-- );