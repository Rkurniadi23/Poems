from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.poem import Poem


# Poem Create Route
@app.route('/poem/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    user=User.get_by_id(session['user_id'])
    return render_template('addPoem.html', user=user)

@app.route('/poem/create/process', methods = ['GET', 'POST'])
def create_poem():
    if 'user_id' not in session:
        return redirect('/')
    if not Poem.validate_poem(request.form):
        return redirect('/poem/create')
    print(request.form)
    data = {
        'user_id': session["user_id"],
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'poem_text': request.form['poem_text']
    }
    Poem.save(data)
    return redirect('/dashboard')

# Poem View Route
# Poem View html hasn't been created (DO NOT FORGET TO CHANGE)***
@app.route('/poem/<int:id>')
def view_poem(id):
    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('viewPoem.html',poem=Poem.get_by_id({'id': id}))

# Poem Edit Route
# Poem Edit html hasn't been created (DO NOT FORGET TO CHANGE)***
@app.route('/poem/edit/<int:id>')
def edit_poem(id):
    if 'user_id' not in session:
        return redirect('/')

    return render_template('editPoem.html',poem=Poem.get_by_id({'id': id}))

@app.route('/poem/update', methods=['POST'])
def update_poem():
    if 'user_id' not in session:
        return redirect('/')
    if not Poem.validate_poem(request.form):
        return redirect(f'/poem/edit/{id}')

    data = {
        "user_id":session['user_id'],
        'id': request.form['id'],
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'poem_text': request.form['poem_text']
    }
    Poem.update(data)
    return redirect('/dashboard')

# Poem Delete Route
@app.route('/poem/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')

    Poem.delete({'id':id})
    return redirect('/dashboard')
