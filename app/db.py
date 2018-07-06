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
    series_number = new_series + new_number
    cur.execute('UPDATE driver SET second_name = ?, first_name =?, middle_name = ?, series_number = ?, block = ?, block_reason = ?, car_id = ? WHERE id = ?',
                [new_second_name, new_first_name, new_middle_nam, series_number, new_block, new_block_reason, new_car_id, driver_id])
    if new_block == 1:
        cur.execute(
            'INSERT INTO event (date, event_type, int_field, txt_field) VALUES (?, ?, ?, ?)',
            [datetime.datetime.now().strftime(time_format), 'add_to_bl', driver_id, new_block_reason]
        )
        conn.commit()
        return
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'update_driver', driver_id]
    )
    conn.commit()


# Get all cars
def get_all_cars():
    conn, cur = get_db()
    car_rows = cur.execute(
        'SELECT id, brand, model, color, year, numberplate, vin, sts, driver_id FROM cars'
    ).fetchall()
    cars = []
    for car_row in car_rows:
        car = {
            'id': car_row[0],
            'brand': car_row[1],
            'model': car_row[2],
            'color': car_row[3],
            'year': car_row[4],
            'numberplate': car_row[5],
            'vin': car_row[6],
            'sts': car_row[7],
            'driver_id': car_row[8]
        }
        cars.append(car)
    return cars


# Get unengaged cars
def get_unengaged_cars():
    cars = get_all_cars()
    unengaged_cars = []
    for car in cars:
        if car['driver_id'] == None:
            unengaged_cars.append(car)
    return unengaged_cars


# Get one car
def get_car(car_id):
    conn, cur = get_db()
    car_row = cur.execute(
        'SELECT brand, model, color, year, numberplate, vin, sts, driver_id FROM cars WHERE id = ?',
        [car_id]
    ).fetchone()
    car = {
        'id': car_id,
        'brand': car_row[0],
        'model': car_row[1],
        'color': car_row[2],
        'year': car_row[3],
        'numberplate': car_row[4],
        'vin': car_row[5],
        'sts': car_row[6],
        'driver_id': car_row[7]
    }
    return car


# Add new car
def add_car(brand, model, color, year, numberplate, vin, sts):
    conn, cur = get_db()
    cur.execute(
        'INSERT INTO cars (brand, model, color, year, numberplate, vin, sts) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [brand, model, color, year, numberplate, vin, sts]
    )
    max_id = cur.execute('SELECT MAX(id) FROM cars').fetchone()
    max_id = max_id[0]
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'add_car', max_id]
    )
    conn.commit()


# Update car
def update_car(car_id, new_brand, new_model, new_color, new_year, new_numberplate, new_vin, new_sts):
    conn, cur = get_db()
    cur.execute('UPDATE cars SET brand = ?, model =?, color = ?, year = ?, numberplate = ?, vin = ?, sts = ? WHERE id = ?',
                [new_brand, new_model, new_color, new_year, new_numberplate, new_vin, new_sts, car_id])
    cur.execute(
        'INSERT INTO event (date, event_type, int_field) VALUES (?, ?, ?)',
        [datetime.datetime.now().strftime(time_format), 'update_driver', car_id]
    )
    conn.commit()


# Change car
def change_car(driver_id, car_id):
    conn, cur = get_db()
    last_car_id = cur.execute('SELECT car_id FROM driver WHERE id = ?', [driver_id]).fetchone()[0]
    if car_id == 0:
        cur.execute('UPDATE driver SET car_id = ? WHERE id = ?', [None, driver_id])
        cur.execute('UPDATE cars SET driver_id = ? WHERE id = ?', [None, last_car_id])
        cur.execute(
            'INSERT INTO event (date, event_type, int_field, txt_field) VALUES (?, ?, ?, ?)',
            [datetime.datetime.now().strftime(time_format), 'return_car', driver_id, car_id]
        )
    else:
        cur.execute('UPDATE driver SET car_id = ? WHERE id = ?', [car_id, driver_id])
        cur.execute('UPDATE cars SET driver_id = ? WHERE id = ?', [driver_id, car_id])
        cur.execute(
            'INSERT INTO event (date, event_type, int_field, txt_field) VALUES (?, ?, ?, ?)',
            [datetime.datetime.now().strftime(time_format), 'get_car', driver_id, car_id]
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
        elif event_type == 'get_car' or event_type == 'return_car':
            driver = get_driver(int_field)
            car = get_car(int_field)
            txt_field = driver['second_name'] + ' ' + driver['first_name'][0] + '.' + driver['middle_name'][0] + '.'
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


# Get acts
def get_acts():
    conn, cur = get_db()
    his = cur.execute('SELECT id, date, int_field, txt_field FROM event WHERE event_type = ?', ['get_car']).fetchall()
    acts = []
    for event in his:
        driver = get_driver(event[2])
        car = get_car(int(event[3]))
        date, time = event[1].split(' ')
        time = time[:-3]
        act = {
            'id': event[0],
            'date': date,
            'time': time,
            'second_name': driver['second_name'],
            'first_name': driver['first_name'],
            'middle_name': driver['middle_name'],
            'brand': car['brand'],
            'model': car['model'],
            'color': car['color'],
            'year': car['year'],
            'numberplate': car['numberplate'],
            'vin': car['vin']
        }
        acts.append(act)
    return acts
