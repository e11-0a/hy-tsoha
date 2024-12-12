from flask import render_template, redirect, g, url_for
from app import app
from db import connection_pool
from model import *
from utils import *


@app.route("/admin", strict_slashes=False)
@requireLogin()
@requireRole(Role.superuser)
def manage_users():
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        users = cur.execute(
            '''SELECT 
            id, username, chosen_name, active, comment,
            array(
            SELECT R.name
            FROM userRoles f, roles R
            WHERE u.id=f.user_id AND f.role_id=R.id
            ) as rol_arr
            FROM users u ORDER BY u.id''').fetchall()
    return render_template("admin.jinja", user=g.user, role=Role, users=users)


@app.route("/toggle/<user>", strict_slashes=False, methods=["POST"])
@requireLogin()
@requireOrigin()
@requireRole(Role.superuser)
def toggle_user(user):
    user_id = int(user)
    if user_id == g.user.id:
        return render_template("error.jinja", error_title="Et voi muokata tiliäsi", error_body="Turvallisuussyistä et voi muokata omaa tiliäsi"), 404

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        user_db = cur.execute(
            '''SELECT active
            FROM users u WHERE u.id=%s''', (user_id,)).fetchone()
        if user_db == None:
            return render_template("error.jinja", error_title="Käyttäjää ei löydy", error_body="Käyttäjää ei löydy"), 404

        active = bool(user_db[0])

        cur.execute("UPDATE users SET active=%s WHERE id=%s", (not active, user_id))             
    return redirect(url_for("manage_users"), 302)