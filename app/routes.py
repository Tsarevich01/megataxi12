import datetime

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm


drive= [
    {
        'fio': 'Иванов А.А.',
        'seriya': '2001',
        'nomer': '123456',
    },
]



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'man'}
    historycar = [

    ]
    return render_template('index.html', title='Home', user=user, posts=historycar)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Авторизация', form=form)


@app.route('/akts')
def akts():
    return render_template('akts.html', title = 'Акты')

@app.route('/drivers')
def drivers():
    driveuser = {'fio': 'ФИО',
                 'seriya': 'Серия паспорта',
                 'nomer': 'Номер паспорта'}

    return render_template('drivers.html', title = 'Водители', drive = drive, driveuser=driveuser)

@app.route('/add_drive')
@app.route('/drivers', methods=['POST', 'GET'])
def add_drive():
    if request.method == 'POST':
        drives = {
            'fio': request.form['fio'],
            'seriya': request.form['seriya'],
            'nomer': request.form['nomer'],

        }
        drive.append(drives)

        flash('Новый пост добавлен')

        return redirect(url_for('drivers'))
    else:
        return render_template('add_drive.html')



@app.route('/car')
#авто
def car():
    usercar = {
        'marka': 'Марка',
        'model': 'Модель',
        'znak': 'Номерной знак'
    }
    car = [
        {
            'marka': 'Lada',
            'model': 'Kalina',
            'znak': "С777СС73",
        },
    ]
    return render_template('car.html', title = 'Машины', car = car, usercar=usercar)

