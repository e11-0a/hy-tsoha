from flask import render_template, request, session, redirect, g, url_for
from functools import wraps
from argon2.exceptions import VerificationError

from app import app
from db import connection_pool
from model import *
import hashing
from config import config


# Initialize user before routing if session exists
@app.before_request
def before_request_callback():
    g.user = None
    if "id" in session:
        if session["id"] != None:
            temp_user = userLoader(session["id"])
            # Deal with deativated users
            if temp_user.active == False:
                # Allow getting static files
                if request.path.startswith("/static/"):
                    pass
                else:
                    return render_template("error.jinja", error_title="Käyttäjätilisi ei ole aktiviinen", error_body="Ota yhteyttä järjestelmänvalvojaan"), 403
            else:
                g.user = temp_user

            g.roles = Role


# Try loading user with id from db
def userLoader(user_id) -> User:
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, active, chosen_name, created, modified, source, comment FROM users WHERE id=%s", (user_id,))
        db_user = cur.fetchone()
        cur.execute(
            "SELECT role_id FROM userRoles WHERE user_id=%s", (user_id,))
        db_roles = list(map(lambda x: x[0], cur.fetchall()))

    return User(
        db_user[0],
        db_user[1],
        db_user[2],
        chosen_name=db_user[3],
        created=db_user[4],
        modified=db_user[5],
        source=db_user[6],
        comment=db_user[7],
        roles=db_roles
    )

# Try loading course with id from db


def getCourse(course_id) -> Course | None:
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        db_course = cur.execute(
            "SELECT id, codename, title, description, mode, code, created, modified FROM courses WHERE id=%s", (course_id,)).fetchone()
        if db_course != None:
            return Course(db_course[0], db_course[1], db_course[2], db_course[3], db_course[4], code=db_course[5], created=db_course[6], modified=[7])
    return None


# Decorator that allows restricting page with role requirement
def requireRole(role=None):
    def roleWrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            if g.user != None:
                if role in g.user.roles:
                    return f(*args, **kwargs)
            return render_template("error.jinja", error_title="Unauthorized", error_body="You're not authorized to view this!"), 403
        return decorated_f
    return roleWrapper

# Decorator that allows restricting page with login requirement


def requireLogin():
    def loginWrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            if g.user != None:
                return f(*args, **kwargs)
            return redirect(url_for('index'), 302)
        return decorated_f
    return loginWrapper


# No CSRF
def requireOrigin():
    def originWrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            # Origin is handled by the browser, so the attacker does not posses enough control over it to
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin
            if "Origin" in request.headers:
                if request.headers["Origin"] == config["security"]["origin"]:
                    return f(*args, **kwargs)
            return "Non-allowed origin"
        return decorated_f
    return originWrapper


# Decorator that allows restricting page with course membership requirement
def verifyCourseAccess():
    def verifyWrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):

            # Do checks for the course parameter
            if "course" not in request.view_args:
                return render_template("error.jinja", error_title="Invalid course", error_body="Course ID has not been provided by caller"), 500
            try:
                course = int(request.view_args["course"])
            except ValueError:
                return render_template("error.jinja", error_title="Invalid course", error_body="Provided course ID not valid"), 400

            # Check the course actually exists
            g.course = getCourse(course_id=course)
            if g.course == None:
                return render_template("error.jinja", error_title="Invalid course", error_body="Course does not exist"), 404

            # If user is logged in
            if g.user != None:
                # And is member of the course
                if g.course.mode > 0:
                    if g.course.isMember(g.user.id):
                        return f(*args, **kwargs)
                    else:
                        return render_template("course-join.jinja", user=g.user, course=g.course, role=Role)

            # Fully open course
            if g.course.mode == 0:
                return f(*args, **kwargs)
            return redirect(url_for('index', 302))
        return decorated_f
    return verifyWrapper
