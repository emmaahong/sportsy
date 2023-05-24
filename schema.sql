DROP TABLE IF EXISTS login;

create table login(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email text not null,
    passcode text not null
);

-- insert into login values(
--     'xyz@gmail.com','XYZ123abc'
-- );


-- IN PROGRESS
create table event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title varchar(255) not null,
  url varchar(255) not null,
  class varchar(255) not null,
  start_date timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  end_date timestamp not null,
  PRIMARY KEY (id)
);
insert into event(id, title, url, class, start_date, end_date) VALUES (1,'Example','http://www.example.com','event-sucess','2019-09-10 20:00:00','2019-09-10 20:01:02');
