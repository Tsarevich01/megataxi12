import db

fixtures_sql = '''
INSERT INTO driver (second_name, first_name, middle_name, series, number, block, block_reason, car_id) VALUES ("Иванов", "Иван", "Иванович", 1337, 123456, null, null, 1);
INSERT INTO driver (second_name, first_name, middle_name, series, number, block, block_reason, car_id) VALUES ("Дмитриев", "Дмитрий", "Дмитриевич", 9876, 999999, 1, "Угнал авто", null);
INSERT INTO driver (second_name, first_name, middle_name, series, number, block, block_reason, car_id) VALUES ("Владимиров", "Владимир", "Владимирович", 8956, 458912, null, null, 2);
INSERT INTO driver (second_name, first_name, middle_name, series, number, block, block_reason, car_id) VALUES ("Алексндров", "Александр", "Александрович", 6548, 985642, null, null, 3);

INSERT INTO car (id, brand, model, vin, sts) VALUES (1, "LADA", "Kalina", 456679, 135487);
INSERT INTO car (id, brand, model, vin, sts) VALUES (2, "RENAULT", "Logan", 987466, 654641);
INSERT INTO car (id, brand, model, vin, sts) VALUES (3, "Lambogini", "Aventador", 146688, 569413);
'''


def run():
    conn, cur = db.get_db()
    cur.executescript(fixtures_sql)
    conn.commit()


if __name__ == "__main__":
    run()
