from app import db


scheme_sql = '''
DROP TABLE IF EXISTS driver
DROP TABLE IF EXISTS car

CREATE TABLE driver (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  second_name TEXT NOT NULL,
  first_name TEXT NOT NULL,
  middle_name TEXT NOT NULL,
  series INTEGER UNIQUE NOT NULL,
  number INTEGER UNIQUE NOT NULL,
  block BOOLEAN NULL,
  block_reason TEXT NULL,
  car_id INTEGER NULL
); 

CREATE TABLE car (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  vin INTEGER UNIQUE NOT NULL,
  sts INTEGER UNIQUE NOT NULL
);
'''


def run():
    conn, cur = db.get_db()
    cur.executescript(scheme_sql)


if __name__ == '__main__':
    run()