from flask_app import app
from flask import request, render_template, redirect, session
from flask_app.models import pie, user
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        return render_template('dashboard.html', user = user.User.get_by_id(user_data), user_pies = pie.Pie.get_by_user_id(user_data))
    return redirect('/')

@app.route('/pie/create', methods = ['POST'])
def add_pie():
    if pie.Pie.validate_pie(request.form):
        pie.Pie.save(request.form)
        return redirect('/dashboard')
    return redirect('/dashboard')

@app.route('/pie/edit/<int:pie_id>')
def edit_pie(pie_id):
    if 'user_id' in session:
        return render_template('edit.html', pie = pie.Pie.get_by_id({'id': pie_id}))
    return redirect('/')

@app.route('/pie/update/<int:pie_id>', methods = ['POST'])
def update_ride(pie_id):
    if pie.Pie.validate_pie(request.form):
        data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'id': pie_id
        }
        pie.Pie.update_pie(data)
        return redirect('/dashboard')
    return redirect(f'/pie/edit/{pie_id}')

@app.route('/pie/delete/<int:pie_id>')
def delete_pie(pie_id):
    if 'user_id' in session:
        pie.Pie.delete_by_id({'id': pie_id})
        return redirect('/dashboard')
    return redirect('/')

@app.route('/pies')
def pie_derby():
    
    return render_template('pie_derby.html', all_pies = pie.Pie.get_all_join_creator())

@app.route('/show/pie/<int:pie_id>')
def show_pie(pie_id):
    if 'user_id' in session:  
        if "count" not in session:
            session["count"] = 0
        return render_template('show_pie.html', pie = pie.Pie.get_all_join_creator_by_id({'id': pie_id}))
    return redirect('/')

@app.route('/pie/vote/<int:pie_id>')
def add_a_vote(pie_id):
    if 'user_id' in session:
        session["count"] = 1
        pie.Pie.add_vote({'id': pie_id})
        return redirect('/pies')
    return redirect('/')

@app.route('/pie/vote/remove/<int:pie_id>')
def delete_vote(pie_id):
    if 'user_id' in session:
        session["count"] = 0
        pie.Pie.delete_vote({'id': pie_id})
        return redirect('/pies')
    return redirect('/')