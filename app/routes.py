from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
import re
import sqlite3
import datetime

# Главная
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'man'}
    history_car = []
    return render_template('index.html', title='Главная', user=user, posts=history_car)


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Авторизация', form=form)


# Акты
@app.route('/acts')
def acts():
    return render_template('acts.html', title='Акты')



@app.route('/acts/<int:driver_id>', methods=['POST', 'GET'])
def act(driver_id):
    akt = db.get_driver(driver_id)


    return render_template('acts_print.html', title='Акт', akt=akt, created=datetime.datetime(2018, 6, 13, 13, 00, 00))


# ЧС
@app.route('/blacklist')
def blacklist():
    blocked_drivers = db.get_blocked_drivers()
    return render_template('blacklist.html', title='Чёрный список', blocked_drivers=blocked_drivers)


# Водители
@app.route('/drivers')
def drivers():
    drivers = db.get_all_drivers()
    return render_template('drivers.html', title='Водители', drivers=drivers)


# Добавить водителя
@app.route('/drivers', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def add_driver():
    if request.method == 'POST':
        second_name = str(request.form['second_name']),
        first_name = str(request.form['first_name']),
        middle_name = str(request.form['middle_name']),
        series = str(request.form['series']),
        number = str(request.form['number'])
        if check_driver_info_errors(second_name, first_name, middle_name, series, number):
            return redirect(url_for('drivers'))
        try:
            db.add_driver(
                second_name= request.form['second_name'],
                first_name= request.form['first_name'],
                middle_name= request.form['middle_name'],
                series= request.form['series'],
                number= request.form['number']
            )
            flash('Новый водитель добавлен')
        except sqlite3.IntegrityError:
            flash('Данные паспорта не могут совпадать с данными паспорта имеющихся водителей!')
        return redirect(url_for('drivers'))
    else:
        return render_template('drivers.html')


# Редактирование водителя
@app.route('/drivers/<int:driver_id>', methods=['POST', 'GET'])
def update_driver(driver_id):
    driver = db.get_driver(driver_id)
    act_cars = db.get_all_cars()
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        new_second_name = request.form['second_name']
        new_first_name = request.form['first_name']
        new_middle_name = request.form['middle_name']
        new_series = request.form['series']
        new_number = request.form['number']
        new_block = request.form['block']
        new_block_reason = request.form['block_reason']
        if check_driver_info_errors(new_second_name, new_first_name, new_middle_name, new_series, new_number):
            return redirect(url_for('drivers'))
        try:
            db.update_driver(driver_id, new_second_name, new_first_name, new_middle_name, new_series, new_number, new_block, new_block_reason)
            flash('Данные о водителе обнавлены')
        except sqlite3.IntegrityError:
            flash('Данные паспорта не могут совпадать с данными паспорта имеющихся водителей!')
        if driver.block == 1:
            return render_template('blacklist.html', driver=driver)
        else:
            return redirect(url_for('drivers'))

    return render_template('update_driver.html', driver=driver, act_cars=act_cars)


# Список авто
@app.route('/cars')
def cars():
    cars = db.get_all_cars()
    return render_template('cars.html', title='Машины', cars=cars)


# Add car
@app.route('/cars', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        numberplate = request.form['numberplate']
        vin = request.form['vin']
        sts = request.form['sts']
        if check_car_info_errors(brand, model, numberplate, vin, sts):
            return redirect(url_for('cars'))
        try:
            db.add_car(
                brand=brand,
                model=model,
                numberplate=numberplate,
                vin=vin,
                sts=sts)
            flash('Новый автомобиль добавлен')
        except sqlite3.IntegrityError:
            flash('Данные номера авто, VIN и СТС не могут совпадать с существующими!')
        return redirect(url_for('cars'))
    else:
        return render_template('cars.html')


# Update car
@app.route('/cars/<int:car_id>', methods=['POST', 'GET'])
def update_car(car_id):
    car = db.get_car(car_id)
    if request.method == 'POST':
        car_id = request.form['car_id']
        new_brand = request.form['brand']
        new_model = request.form['model']
        new_numberplate = request.form['numberplate']
        new_vin = request.form['vin']
        new_sts = request.form['sts']
        if check_car_info_errors(new_brand, new_model, new_numberplate, new_vin, new_sts):
            return redirect(url_for('cars'))
        try:
            db.update_car(car_id, new_brand, new_model, new_numberplate, new_vin, new_sts)
            flash('Данные о автомобиле обнавлены')
        except sqlite3.IntegrityError:
            flash('Данные номера авто, VIN и СТС не могут совпадать с существующими!')
        return redirect(url_for('cars'))
    return render_template('update_car.html', car=car)


# Тут у нас валидаторы
# Проверка инфы о водителе
def check_driver_info_errors(second_name, first_name, middle_name, series, number):
    second_name = second_name[0]
    first_name = first_name[0]
    middle_name = middle_name[0]
    series = series[0]
    flash_list = []
    if not re.fullmatch('[А-ЯЁ][а-яё]{,14}', second_name):
        flash_list.append(
            'Фамилия должна состоять из кириллических букв, начинаться с заглавной и в длине не превышать 15 символов!'
        )
    if not re.fullmatch('[А-ЯЁ][а-яё]{,14}', first_name):
        flash_list.append(
            'Имя должно состоять из кириллических букв, начинаться с заглавной и в длине не превышать 15 символов!'
        )
    if not re.fullmatch('[А-ЯЁ][а-яё]{,14}', middle_name):
        flash_list.append(
            'Отчество должно состоять из кириллических букв, начинаться с заглавной и в длине не превышать 15 символов!'
        )
    if not re.fullmatch('\d{4}', str(series)):
        flash_list.append('Серия состоит строго из 4-х цифр!')
    if not re.fullmatch('\d{6}', str(number)):
        flash_list.append('Номер состоит строго из 6 цифр!')
    if flash_list:
        for message in flash_list:
            flash(message)
        return True
    return False


# Проверка инфы об авто
def check_car_info_errors(brand, model, numberplate, vin, sts):
    # form = {
    #     "brand": brand,
    #     "model": model,
    #     "numberplate": numberplate,
    #     "vin": vin,
    #     "sts": sts
    # }
    flash_list = []
    print(type(brand))
    if not re.fullmatch('[A-Z][a-z]{,14}', brand):
        flash_list.append(
            'Название марки авто пишется латинскими буквами, начинается с заглавной буквы и не может превышать 15 симовлов в длине!')
    if not re.fullmatch('[A-Z][a-zA-Z]{,14}', model):
        flash_list.append(
            'Название модели авто пишется латинскими буквами, начинается с заглавной буквы и не может превышать 15 симовлов в длине!')
    if not re.fullmatch('[А-ЯЁ]\d{3}[А-ЯЁ]{2}\d{2,3}', numberplate):
        flash_list.append('Неверно введён номер. Примеры правилно введённого номера: А777МД73, В666АД199')
    if not re.fullmatch('[A-Z1-9]{17}', vin):
        flash_list.append('Неправильно введён VIN. Он состоит из 17 латинских симовлов или арабских цифр!')
    if not re.fullmatch('\d{10}', sts):
        flash_list.append('Неправильно введён номер СТС. Он состоит строго из 10 цифр!')
    if flash_list:
        for message in flash_list:
            flash(message)
        return True
    return False
# clone, pull, checkout
