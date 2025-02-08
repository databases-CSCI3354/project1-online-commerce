import sqlite3
from flask import Blueprint, jsonify, render_template, request, current_app, g, url_for, redirect
from flask_login import login_required
from flask_bcrypt import Bcrypt 

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


DATABASE = 'C:\\Users\\nuhin\\git\\project1-online-commerce\\northwind.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


@auth_bp.route("/login", methods=["POST"])
def login():
    """Handle user login"""
    data = request.get_json()
    # Add your login logic here
    username = request.get('username')
    password = request.get('password')
    validate_user = validate(username, password)
    if validate_user == False:
        error = 'Invalid Credentials Please Try Again'
        return render_template('index.html', error=error)
    else:
        return redirect(url_for('loggedin'))
    return render_template('index.html', error=error)
    return jsonify({"message": "Login endpoint"})

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password) 

def validate(username, password):
    g.db = get_db()
    user = query_db('SELECT * FROM Users WHERE username = ?',
                    [username], one=True)

    return False if user is None else check_password(user['password'], password)


@auth_bp.route("/profile")
@login_required
def profile():
    """Protected profile route"""
    return render_template("auth/profile.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Handle user logout"""
    # Add your logout logic here
    return jsonify({"message": "Logged out successfully"})
