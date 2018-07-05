import db

schema_sql = '''
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS cars;

CREATE TABLE driver (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  second_name TEXT NOT NULL,
  first_name TEXT NOT NULL,
  middle_name TEXT NULL,
  series INTEGER UNIQUE NOT NULL,
  number INTEGER UNIQUE NOT NULL,
  block bit NOT NULL DEFAULT 0,
  block_reason TEXT NULL,
  car_id INTEGER UNIQUE NULL
); 

CREATE TABLE cars (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  numberplate TEXT UNIQUE NOT NULL,
  vin TEXT UNIQUE NOT NULL,
  sts TEXT UNIQUE NOT NULL,
  driver_id INTEGER UNIQUE NULL 
);
'''
# Сканов нема


def run():
    conn, cur = db.get_db()
    cur.executescript(schema_sql)


if __name__ == '__main__':
    run()
