import sqlite3


def get_db():
    conn = sqlite3.connect('DataBase.db')
    cur = conn.cursor()
    return conn, cur


# all drivers
def get_all_drivers():
    conn, cur = get_db()
    driver_rows = cur.execute(
        'SELECT id, second_name, first_name, middle_name, series, number, block, block_reason, car_id FROM driver ORDER BY DESC'
                              ).fetchall()
    drivers = []
    for driver_row in driver_rows:
        driver = {
            "id": driver_row[0],
            "second_name": driver_row[1],
            "first_name": driver_row[2],
            "middle_name": driver_row[3],
            "series": driver_row[4],
            "number": driver_row[5],
            "block": driver_row[6],
            "block_reason": driver_row[7],
            "car_id": driver_row[8]
        }
        drivers.append(driver)
    return drivers


# one driver
def get_driver(driver_id):
    conn, cur = get_db()
    driver_row = cur.execute(
        'SELECT second_name, first_name, middle_name, series, number, block, block_reason, car_id FROM driver WHERE id = ?', [driver_id]
    ).fetchone()
    driver = {
        "id": driver_id,
        "second_name": driver_row[0],
        "first_name": driver_row[1],
        "middle_name": driver_row[2],
        "series": driver_row[3],
        "number": driver_row[4],
        "block": driver_row[5],
        "block_reason": driver_row[6],
        "car_id": driver_row[7]
    }
    return driver


# add new driver
def add_driver(second_name, first_name, middle_name, series, number, car_id):
    conn, cur = get_db()
    cur.execute(
        'INSERT INTO driver (second_name, first_name, middle_name, series, number, car_id) VALUES (?, ?, ?, ?, ?, ?)',
        [second_name, first_name, middle_name, series, number, car_id]
    )
    conn.commit()

# all cars
def get_all_cars():
    return cars

# one car
def get_car():
    return car


#add new car
def add_car():
    conn.commit()


if __name__ == '__main__':
    from app import init_db as idb
    idb.run()
