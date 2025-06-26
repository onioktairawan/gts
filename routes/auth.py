from flask import Blueprint, request, redirect, session, render_template
from models.db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    users = db['users']
    message = None
    if request.method == 'POST':
        user = users.find_one({
            'username': request.form['username'],
            'password': request.form['password']
        })
        if user:
            session['username'] = user['username']
            return redirect('/')
        else:
            message = "Username atau password salah."
    return render_template('login.html', title='Login', message=message)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    users = db['users']
    message = None
    if request.method == 'POST':
        if users.find_one({'username': request.form['username']}):
            message = "Username sudah digunakan."
        else:
            users.insert_one({
                'username': request.form['username'],
                'password': request.form['password']
            })
            message = "Berhasil mendaftar, silakan login."
            return redirect('/login')
    return render_template('login.html', title='Register', message=message)

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
