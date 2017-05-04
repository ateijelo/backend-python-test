CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE todos (
  id INTEGER PRIMARY KEY,
  user_id INT(11) NOT NULL,
  description VARCHAR(255),
  completed BOOLEAN,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

PRAGMA user_version = 2017050300;
