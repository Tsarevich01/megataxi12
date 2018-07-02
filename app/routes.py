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


# Редактирование водителя
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
        new_block = request.form['block']
        new_block_reason = request.form['block_reason']
        db.update_driver(driver_id, new_second_name, new_first_name, new_middle_name, new_series, new_number, new_block, new_block_reason)

        flash('Данные о водителе обнавлены')
        if driver.block == 1:
            return render_template('blacklist.html', driver=driver)
        else:
            return redirect(url_for('drivers'))

    return render_template('update_driver.html', driver=driver)


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
        if not check_car_info(brand, model, numberplate, vin, sts):
            return redirect(url_for('cars'))
        db.add_car(
            brand=brand,
            model=model,
            numberplate=numberplate,
            vin=vin,
            sts=sts)
        flash('Новый автомобиль добавлен')
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
        if not check_car_info(new_brand, new_model, new_numberplate, new_vin, new_sts):
            return redirect(url_for('cars'))
        db.update_car(car_id, new_brand, new_model, new_numberplate, new_vin, new_sts)

        flash('Данные о автомобиле обнавлены')

        return redirect(url_for('cars'))
    return render_template('update_car.html', car=car)


# Проверка инфы об авто
def check_car_info(brand, model, numberplate, vin, sts):
    if len(numberplate) > 9:
        flash('Длина номера не может превышать 9 знаков!')
        return False
    return True
