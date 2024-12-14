from flask import render_template, redirect, g, url_for

from app import app
from db import connection_pool
from model import *
from utils import *

from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    return render_template("500.jinja", e=e), 500



@app.route("/")
def index():
    if g.user:
        return redirect(url_for('my_index'), 302)
    return render_template("login.jinja")



@app.route("/my", strict_slashes=False)
@requireLogin()
def my_index():
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_list: list[Course] = list(map(lambda x: Course(x[0], x[1], x[2], x[3], x[4], code=x[5], created=x[6], modified=[7]), cur.execute(
            "SELECT C.id, C.codename, C.title, C.description, C.mode, C.code, C.created, C.modified FROM courses C, courseMembers WHERE C.id=courseMembers.course_id AND courseMembers.user_id=%s", (g.user.id,)).fetchall()))
    return render_template("my-page.jinja", user=g.user, courses=course_list)

@app.route("/me", strict_slashes=False)
@requireLogin()
def my_account():
    return render_template("me.jinja", user=g.user)

