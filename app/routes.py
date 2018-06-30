import datetime

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm

drivers = [
    {
        'second_name': 'Иванов',
        'first_name': 'Иван',
        'middle_name': 'Иванович',
        'series': '2001',
        'number': '123456',
    }
]


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


# ЧС
@app.route('/blacklist')
def blacklist():
    return render_template('blacklist.html', title='Чёрный список')


# Водители
@app.route('/driverst')
def driverst():
    # Это зачем??
    driveuser = {'fio': 'ФИО',
                 'series': 'Серия паспорта',
                 'number': 'Номер паспорта'}
    # Вот сверху

    return render_template('drivers.html', title='Водители', drivers=drivers, driveuser=driveuser)


# Добавить водителя
@app.route('/driverst')
@app.route('/add_drive', methods=['POST', 'GET'])
def add_driver():
    if request.method == 'POST':
        db.add_driver(
            second_name= request.form['second_name'],
            first_name= request.form['first_name'],
            middle_name= request.form['middle_name'],
            series= request.form['series'],
            number= request.form['number'],
            car_id = request.form['car_id'])






        flash('Новый водитель добавлен')

        return redirect(url_for('driverst'))
    else:

        return render_template('add_driver.html')


# Авто
@app.route('/car')
def car():
    # И это почто?
    user_car = {
        'brand': 'Марка',
        'model': 'Модель',
        'numberplate': 'Номерной знак'
    }
    # Вверху
    cars = [
        {
            'brand': 'Lada',
            'model': 'Kalina',
            'numberplate': "С777СС73"
        }
    ]
    return render_template('cars.html', title='Машины', cars=cars, user_car=user_car)

@app.route('/car')
@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        db.add_car(
            brand= request.form['brand'],
            model= request.form['model'],
            numberlate= request.form['numberlate'],
            vin= request.form['vin'],
            sts= request.form['sts'])






        flash('Новый автомобиль добавлен')

        return redirect(url_for('car'))
    else:

        return render_template('add_car.html')