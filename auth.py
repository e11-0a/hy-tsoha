from flask import render_template, request, session, redirect, g, url_for
from argon2.exceptions import VerificationError

from app import app
from db import connection_pool
from utils import *
from model import *
import hashing


@app.route("/register")
def register():
    if g.user:
        return redirect(url_for('my_index'), 302)
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        is_registering_admin = cur.execute(
            'SELECT COUNT(*) FROM users').fetchone()[0] == 0
    return render_template("register.jinja", createAdmin=is_registering_admin)


@app.route("/register", methods=["POST"])
@requireOrigin()
def register_submit():
    if g.user:
        return redirect(url_for('my_index'), 302)
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        is_registering_admin = cur.execute(
            'SELECT COUNT(*) FROM users').fetchone()[0] == 0

        if g.user:
            return redirect(url_for('my_index'), 302)

        user_type = request.form["type"]
        if not (user_type in ["student", "teacher"]):
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Käyttäjätyyppi ei kelpaa")
        else:
            user_type = {
                "student": 2,
                "teacher": 1
            }[user_type]

        username = request.form["username"]
        if (len(username) < 3) or (not username.isalnum()):
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Käyttäjänimi ei kelpaa")

        password = request.form["password"]
        password_verify = request.form["password-verify"]
        if (password != password_verify):
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Salasanat eivät täsmää")
        if (len(password) > 63):
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Salasana ei kelpaa (yli 64 merkkiä)")
        if (len(password) < 8):
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Salasana ei kelpaa (alle 8 merkkiä)")

        hashed_password = hashing.tryHash(password)

        print(username, password, password_verify)

        is_name_available = cur.execute(
            'SELECT COUNT(*) FROM users WHERE username=%s', (username,)).fetchone()[0] == 0

        if is_name_available:
            pass
        else:
            return render_template("register.jinja", createAdmin=is_registering_admin, error="Toinen käyttäjä samalla nimellä on jo olemassa")

        print(hashed_password)

        user = cur.execute('INSERT INTO users (username, chosen_name, password, active, source, comment) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;',
                           (username, username, hashed_password, True, 1, "Created with self-register")).fetchone()[0]

        cur.execute(
                'INSERT INTO userRoles (user_id, role_id) VALUES (%s, %s);', (user, user_type))


        if is_registering_admin:
            cur.execute(
                'INSERT INTO userRoles (user_id, role_id) VALUES (%s, 3);', (user,))

    return redirect(url_for('my_index'), 302)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    session["id"] = None
    return redirect("/")


@app.route("/login", methods=["POST"])
@requireOrigin()
def login():
    username = request.form["username"]
    password = request.form["password"]

    if (username == None) or (password == None):
        return redirect(url_for('index'), 302)
    db_user = None
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password FROM users WHERE username=%s", (username,))
        db_user = cur.fetchone()
    if db_user == None:
        return redirect(url_for('index'), 302)

    verify_result = False
    try:
        verify_result = hashing.tryVerify(db_user[2], password)

    except VerificationError as e:
        print(f"[auth] Invalid login attempt for: {username}")

    if verify_result:
        session["username"] = username
        session["id"] = db_user[0]

    return redirect(url_for('index'), 302)
