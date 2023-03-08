from flask_app import app
from flask import Flask, redirect, render_template, request, session, flash
from flask_app.models.user import User
from flask_app.models.journal import Journal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration')
def registration():
    return render_template("register.html")
    

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect ('/registration')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id =User.save_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user_id = User.get_by_email(data)
    print(request.form)
    if not user_id:
        flash('Email or Password Incorrect','login')
        print("Craziness")
        return redirect('/')
    if not bcrypt.check_password_hash(user_id.password,request.form['password']):
        flash('Email or Password Incorrect','login')
        print('Password cooky')
        return redirect('/')

    session['user_id']=user_id.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')