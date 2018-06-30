import sqlite3


def get_db():
    conn = sqlite3.connect('DataBase.db')
    cur = conn.cursor()
    return conn, cur


# All drivers
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


# One driver
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


# Add new driver
def add_driver(second_name, first_name, middle_name, series, number, car_id):
    conn, cur = get_db()
    cur.execute(
        'INSERT INTO driver (second_name, first_name, middle_name, series, number, car_id) VALUES (?, ?, ?, ?, ?, ?)',
        [second_name, first_name, middle_name, series, number, car_id]
    )
    conn.commit()


# Get all cars
def get_all_cars():
    conn, cur = get_db()
    car_rows = cur.execute(
        'SELECT id, brand, model, numberplate, vin, sts FROM cars ORDER BY DESC '
    ).fetchall()
    cars = []
    for car_row in car_rows:
        cars = {
            'id': car_row[0],
            'brand': car_row[1],
            'model': car_row[2],
            'numberplate': car_row[3],
            'vin': car_row[4],
            'sts': car_row[5]
        }
    return cars


# Get one car
def get_car(car_id):
    conn, cur = get_db()
    car_row = cur.execute(
        'SELECT brand, model, numberplate, vin, sts FROM cars WHERE id = ?',
        [car_id]
    ).fetchone()
    car = {
        'id': car_id,
        'brand': car_row[0],
        'model': car_row[1],
        'numberplate': car_row[2],
        'vin': car_row[3],
        'sts': car_row[4]
    }
    return car


# Add new car
def add_car(brand, model, numberplate, vin, sts):
    conn, cur = get_db()
    cur.execute(
        'INSERT INTO car (brand, model, numberplate, vin, sts) VALUES (?, ?, ?, ?, ?)',
        [brand, model, numberplate, vin, sts]
    )
    conn.commit()


if __name__ == '__main__':
    from app.database import init_db as idb

    idb.run()