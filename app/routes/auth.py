import sqlite3
from flask import Blueprint, current_app, g, jsonify, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_required

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
    username = data.get('username')
    password = data.get('password')
    validate_user = validate(username, password)
    if validate_user is None:
        error = 'Invalid Credentials Please Try Again'
        return render_template('index.html', error=error)
    else:
        return redirect(url_for('profile'))
    return jsonify({"message": "Login endpoint"})

@auth_bp.route("/register", methods=["POST"])
def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        g.db = get_db()
        try:
            g.db.execute(
                'INSERT INTO Users (username, hashed_password) VALUES (?, ?)',
                (username, hashed_password)
            )
            g.db.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "Username already exists"}), 400
        return jsonify({"message": "Register endpoint"})

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password) 

def validate(username, password):
    user = query_db('SELECT * FROM Users WHERE username = ?', [username], one=True)
    print(type(user))
    if user is None or not check_password(dict(user)['hashed_password'], password):
        return None
    return user


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
