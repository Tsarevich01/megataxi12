import sqlite3


def get_db():
    conn = sqlite3.connect('DataBase.db')
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    from app import init_db as idb
    idb.run()
