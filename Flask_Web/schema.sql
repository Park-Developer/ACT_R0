DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user_list;

/*필요없읃듯*/
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  type TEXT NOT NULL,
  view INTEGER,
  like_num INTEGER,
  dislike_num INTEGER,
  FOREIGN KEY (author_id) REFERENCES user_list (id)
);

CREATE TABLE user_list (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  tier TEXT DEFAULT 'Bronze',
  login_state TEXT DEFAULT 'Temp',
  profile_img_addr TEXT,
  telegram_api TEXT UNIQUE,
  access_code TEXT UNIQUE,
  access_code_time TEXT UNIQUE,
  upbit_access_key TEXT UNIQUE,
  upbit_secret_key TEXT UNIQUE,
  allowed_ip TEXT,
  target_coin TEXT,
  balance_update_time TEXT DEFAULT CURRENT_TIMESTAMP,
  current_cash_balance TEXT,
  current_coin_list TEXT
);
