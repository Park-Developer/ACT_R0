DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user_list;
DROP TABLE IF EXISTS strategy;

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  type TEXT NOT NULL,
  view_num INTEGER DEFAULT 0,
  like_num INTEGER DEFAULT 0,
  dislike_num INTEGER DEFAULT 0,
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
  target_coin1 JSON DEFAULT ('{}'),
  target_coin2 JSON DEFAULT ('{}'),
  target_coin3 JSON DEFAULT ('{}'),
  target_coin4 JSON DEFAULT ('{}'),
  target_coin5 JSON DEFAULT ('{}'),
  balance_update_time TEXT DEFAULT CURRENT_TIMESTAMP,
  current_cash_balance TEXT,
  write_post TEXT,
  view_post TEXT,
  like_post TEXT,
  dislike_post TEXT
);

CREATE TABLE strategy (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  introduction TEXT,
  code TEXT NOT NULL,
  link TEXT NOT NULL,
  version TEXT NOT NULL,
  developer TEXT NOT NULL,
  contributor TEXT NOT NULL,
  update_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  inquery TEXT,
  dynamic_ref INTEGER,
  monitoring_time TEXT,
  dynamic_bid INTEGER,
  minute_unit INTEGER,
  past_data_count INTEGER,
  bid_price_condition1 INTEGER,
  dynamic_ask INTEGER,
  ask_price_condition1 INTEGER

);
