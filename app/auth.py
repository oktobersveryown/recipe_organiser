from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_database_connection


class User(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = get_database_connection()
        user_data = conn.execute(
            "SELECT id, username, password FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if user_data:
            return User(user_data["id"], user_data["username"], user_data["password"])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_database_connection()
        user_data = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        if user_data:
            return User(user_data["id"], user_data["username"], user_data["password"])
        return None


def load_user(user_id):
    return User.get(user_id)


def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            flash("Username and password are required!", "error")
        else:
            conn = get_database_connection()
            existing_user = conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if existing_user:
                flash("Username already exists!", "error")
            else:
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256"
                )
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password),
                )
                conn.commit()
                conn.close()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))
    return render_template("register.html")


def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_database_connection()
        user_data = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data["id"], user_data["username"], user_data["password"])
            login_user(user)
            flash("Logged in successfully!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")


def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
