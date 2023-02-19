from flask_app import app
from flask import request, render_template, redirect, session, flash
from flask_app.models import user, pie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/')
def login_register():
    return render_template('login_register.html')

@app.route('/login', methods=['POST'])
def login():
    this_user = user.User.get_by_email(request.form)
    print(this_user)
    if this_user:
        if bcrypt.check_password_hash(this_user.password, request.form['password']):
            session['user_id'] = this_user.id
            return redirect('/dashboard')
    
    flash("Invalid Credentials", 'logError')
    return redirect('/')

@app.route('/register', methods=['POST'])
def reg():
    if user.User.validate_user(request.form):
        hashed_pass = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashed_pass
        }
        user_id = user.User.save(data)
        session['user_id'] = user_id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

