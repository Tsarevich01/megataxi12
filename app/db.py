import datetime
import sqlite3


time_format = '%d.%m.%Y %H:%M:%S'


# Get DB
def get_db():
    conn = sqlite3.connect('DataBase.db')
    cur = conn.cursor()
    return conn, cur


# All drivers
def get_all_drivers():
    conn, cur = get_db()
    driver_rows = cur.execute(
        'SELECT id, second_name, first_name, middle_name, series_number, block, block_reason, car_id FROM driver'
                              ).fetchall()
    drivers = []
    for driver_row in driver_rows:
        driver = {
            "id": driver_row[0],
            "second_name": driver_row[1],
            "first_name": driver_row[2],
            "middle_name": driver_row[3],
            "series": driver_row[4][:4],
            "number": driver_row[4][4:],
            "block": driver_row[5],
            "block_reason": driver_row[6],
            "car_id": driver_row[7]
        }
        drivers.append(driver)
    return drivers


# One driver
def get_driver(driver_id):
    conn, cur = get_db()
    driver_row = cur.execute(
        'SELECT second_name, first_name, middle_name, series_number, block, block_reason, car_id FROM driver WHERE id = ?', [driver_id]
    ).fetchone()
    driver = {
        "id": driver_id,
        "second_name": driver_row[0],
        "first_name": driver_row[1],
        "middle_name": driver_row[2],
        "series": driver_row[3][:4],
        "number": driver_row[3][4:],
        "block": driver_row[4],
        "block_reason": driver_row[5],
        "car_id": driver_row[6]
    }
    return driver


# Get blocked drivers
def get_blocked_drivers():
    conn, cur = get_db()
    driver_rows = cur.execute(
        'SELECT id, second_name, first_name, middle_name, series_number, block_reason FROM driver WHERE block = 1'
    ).fetchall()
    drivers = []
    for driver_row in driver_rows:
        driver = {
            "id": driver_row[0],
            "second_name": driver_row[1],
            "first_name": driver_row[2],
            "middle_name": driver_row[3],
            "series": driver_row[4][:4],
            "number": driver_row[4][:4],
            "block_reason": driver_row[5]
        }
        drivers.append(driver)
    return drivers


# Add new driver
def add_driver(second_name, first_name, middle_name, series, number):
    conn, cur = get_db()
    series_number = series + number
    cur.execute(
        'INSERT INTO driver (second_name, first_name, middle_name, series_number) VALUES (?, ?, ?, ?)',
        [second_name, first_name, middle_name, series_number]
    )
    max_id = cur.execute('SELECT MAX(id) FROM driver').fetchone()
    max_id = max_id[0]
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'add_driver', max_id]
    )
    conn.commit()


# Update driver
def update_driver(driver_id, new_second_name, new_first_name, new_middle_nam, new_series, new_number, new_block=0, new_block_reason=None, new_car_id = None):
    conn, cur = get_db()
    last_car_id = cur.execute('SELECT car_id FROM driver WHERE id=?',[driver_id]).fetchone()[0]
    series_number = new_series + new_number
    cur.execute('UPDATE driver SET second_name = ?, first_name =?, middle_name = ?, series_number = ?, block = ?, block_reason = ?, car_id = ? WHERE id = ?',
                [new_second_name, new_first_name, new_middle_nam, series_number, new_block, new_block_reason, new_car_id, driver_id])
    if new_block == 1:
        cur.execute(
            'INSERT INTO event (date, event_type, int_field, text_field) VALUES (?, ?, ?, ?)',
            [datetime.datetime.now().strftime(time_format), 'add_to_bl', driver_id, new_block_reason]
        )
        conn.commit()
        return
    elif new_car_id != last_car_id:
        cur.execute(
            'INSERT INTO event (date, event_type, int_field, text_field) VALUES (?, ?, ?, ?)',
            [datetime.datetime.now().strftime(time_format), 'change_car', driver_id, str(new_car_id)]
        )
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'update_driver', driver_id]
    )
    conn.commit()


# Get all cars
def get_all_cars():
    conn, cur = get_db()
    car_rows = cur.execute(
        'SELECT id, brand, model, numberplate, vin, sts, driver_id FROM cars'
    ).fetchall()
    cars = []
    for car_row in car_rows:
        car = {
            'id': car_row[0],
            'brand': car_row[1],
            'model': car_row[2],
            'numberplate': car_row[3],
            'vin': car_row[4],
            'sts': car_row[5],
            'driver_id': car_row[6]
        }
        cars.append(car)
    return cars


# Get one car
def get_car(car_id):
    conn, cur = get_db()
    car_row = cur.execute(
        'SELECT brand, model, numberplate, vin, sts, driver_id FROM cars WHERE id = ?',
        [car_id]
    ).fetchone()
    car = {
        'id': car_id,
        'brand': car_row[0],
        'model': car_row[1],
        'numberplate': car_row[2],
        'vin': car_row[3],
        'sts': car_row[4],
        'driver_id': car_row[5]
    }
    return car


# Add new car
def add_car(brand, model, numberplate, vin, sts):
    conn, cur = get_db()
    cur.execute(
        'INSERT INTO cars (brand, model, numberplate, vin, sts) VALUES (?, ?, ?, ?, ?)',
        [brand, model, numberplate, vin, sts]
    )
    max_id = cur.execute('SELECT MAX(id) FROM cars').fetchone()
    max_id = max_id[0]
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'add_car', max_id]
    )
    conn.commit()


# Update car
def update_car(car_id, new_brand, new_model, new_numberplate, new_vin, new_sts):
    conn, cur = get_db()
    cur.execute('UPDATE cars SET brand = ?, model =?, numberplate = ?, vin = ?, sts = ? WHERE id = ?',
                [new_brand, new_model, new_numberplate, new_vin, new_sts, car_id])
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'update_driver', car_id]
    )
    conn.commit()


# Get history
def get_history():
    conn, cur = get_db()
    his_rows = cur.execute('SELECT date, event_type, int_field, txt_field FROM event').fetchall()
    his = []
    for his_row in his_rows:
        event_type = his_row[1]
        int_field = his_row[2]
        txt_field = his_row[3]
        additional_field = None
        if event_type == 'add_driver' or event_type == 'update_driver':
            driver = get_driver(int_field)
            txt_field = driver['second_name'] + ' ' + driver['first_name']
        elif event_type == 'add_car' or event_type == 'update_car':
            car = get_car(int_field)
            txt_field = car['brand'] + ' ' + car['model'] + ' ' + car['numberplate']
        elif event_type == 'add_to_bl':
            driver = get_driver(int_field)
            additional_field = driver['second_name'] + ' ' + driver['first_name']
        elif event_type == 'change_car':
            driver = get_driver(int_field)
            car = get_car(int_field)
            txt_field = driver['second_name'] + ' ' + driver['first_name']
            additional_field = car['brand'] + ' ' + car['model'] + ' ' + car['numberplate']
        event = {
            'date': his_row[0],
            'event_type': event_type,
            'int_field': int_field,
            'txt_field': txt_field,
            'additional_field': additional_field
        }
        his.append(event)
    return his
