from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm


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
@app.route('/drivers')
def drivers():
    # Это зачем??
    driveuser = {'fio': 'ФИО',
                 'series': 'Серия паспорта',
                 'number': 'Номер паспорта'}

    # Вот сверху
    drivers = db.get_all_drivers()
    return render_template('drivers.html', title='Водители', drivers=drivers, driveuser=driveuser)


# Добавить водителя
@app.route('/drivers', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def add_driver():
    if request.method == 'POST':
        db.add_driver(
            second_name= request.form['second_name'],
            first_name= request.form['first_name'],
            middle_name= request.form['middle_name'],
            series= request.form['series'],
            number= request.form['number']
        )

        flash('Новый водитель добавлен')

        return redirect(url_for('drivers'))
    else:
        return render_template('drivers.html')

@app.route('/drivers/<int:driver_id>', methods=['POST', 'GET'])
def update_driver(driver_id):
    driver = db.get_driver(driver_id)
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        new_second_name = request.form['second_name']
        new_first_name = request.form['first_name']
        new_middle_name = request.form['middle_name']
        new_series = request.form['series']
        new_number = request.form['number']
        db.update_driver(driver_id, new_second_name, new_first_name, new_middle_name, new_series, new_number)

        flash('Данные о водителе обнавлены')

        return redirect(url_for('drivers'))
    return render_template('update_driver.html', driver=driver)


# Сптсок авто
@app.route('/cars')
def cars():
    # И это почто?
    user_car = {
        'brand': 'Марка',
        'model': 'Модель',
        'numberplate': 'Номерной знак'
    }
    # Вверху
    cars = db.get_all_cars()
    return render_template('cars.html', title='Машины', cars=cars, user_car=user_car)


# Add car
@app.route('/cars', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        db.add_car(
            brand= request.form['brand'],
            model= request.form['model'],
            numberplate= request.form['numberplate'],
            vin= request.form['vin'],
            sts= request.form['sts'])

        flash('Новый автомобиль добавлен')

        return redirect(url_for('cars'))
    else:

        return render_template('cars.html')
