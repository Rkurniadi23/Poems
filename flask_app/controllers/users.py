from flask_app import app
from flask_app.models.user import User
from flask_app.models.poem import Poem
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash

# User Login Route
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email.", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')

# User Registration Route
@app.route('/signup')
def signup():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect("/signup")
    email = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email)
    if user_in_db:
        flash("An account is already using that email. Please use another email address.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard') 

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_by_id(session['user_id'])
    poems = Poem.get_all()
    my_poems = Poem.get_all_from_user(session['user_id'])
    return render_template('dash.html', user=user, poems=poems, my_poems=my_poems)

# User Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")