from flask import render_template, request, session, redirect, g, url_for
from functools import wraps
from argon2.exceptions import VerificationError

from app import app
from db import connection_pool
from model import *
import hashing


# Initialize user before routing if session exists
@app.before_request
def before_request_callback():
    g.user = None
    if "id" in session:
        if session["id"] != None:
            g.user = userLoader(session["id"])
            g.roles = Role
    print("Before request", session)


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
    if db_user == None:
        raise Exception("No user with id", user_id)
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


# Decorator that allows restricting page with course membership requirement
def verifyCourseAccess():
    def verifyWrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):

            # Do checks for the course parameter
            if "course" not in request.view_args:
                return render_template("error.jinja", error_title="Generic error", error_body="Generic routing error"), 404
            try:
                course = int(request.view_args["course"])
            except ValueError:
                return render_template("error.jinja", error_title="Generic error", error_body="Generic routing error"), 404

            # Check the course actually exists
            g.course = getCourse(course_id=course)
            if g.course == None:
                return render_template("error.jinja", error_title="Generic error", error_body="Generic routing error"), 404

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


@app.route("/courses", strict_slashes=False)
@requireLogin()
def course_index():
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_list: list[Course] = list(map(lambda x: Course(x[0], x[1], x[2], x[3], x[4], code=x[5], created=x[6], modified=[7]), cur.execute(
            "SELECT id, codename, title, description, mode, code, created, modified FROM courses").fetchall()))
    return render_template("courses.jinja", user=g.user, courses=course_list)


@app.route("/courses/<course>", strict_slashes=False)
@verifyCourseAccess()
def course_page(course):
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))
    return render_template("course.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=None, role=Role)


@app.route("/courses/<course>/<material>", strict_slashes=False)
@verifyCourseAccess()
def course_material_page(course, material):
    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Material not found!", error_body="material not found"), 404

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))

        db_current_material = cur.execute(
            'SELECT id, name, material_type, content FROM courseMaterials WHERE course_id=%s AND id=%s', (g.course.id, material)).fetchone()

        if db_current_material == None:
            return render_template("error.jinja", error_title="Material not found!", error_body="material not found"), 404

        # Loaded as necessary, so not populated by default
        current_material.name = db_current_material[1]
        current_material.type = int(db_current_material[2])
        current_material.content = db_current_material[3]
    return render_template("course.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=current_material, role=Role)


@app.route("/edit/courses/<course>/<material>", strict_slashes=False)
@verifyCourseAccess()
@requireRole(Role.teacher)
def course_material_edit(course, material):
    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Material not found!", error_body="material not found"), 404

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))

        db_current_material = cur.execute(
            'SELECT id, name, material_type, content FROM courseMaterials WHERE course_id=%s AND id=%s', (g.course.id, material)).fetchone()

        if db_current_material == None:
            return render_template("error.jinja", error_title="Material not found!", error_body="material not found"), 404
        
        # Loaded as necessary, so not populated by default
        current_material.name = db_current_material[1]
        current_material.type = int(db_current_material[2])
        current_material.content = db_current_material[3]
    return render_template("course_editor.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=current_material, role=Role)

# Save material edits
@app.route("/edit/courses/<course>/<material>", strict_slashes=False, methods=['POST'])
@verifyCourseAccess()
@requireRole(Role.teacher)
def save_course_material(course, material):
    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Material not found!", error_body="material not found"), 404

    # TODO: solve flask's POST max size

    #with connection_pool.connection() as conn:
    #    cur = conn.cursor()
    #    cur.execute(
    #        'UPDATE courseMaterials SET content=%s WHERE id=%s AND course_id=%s', (data, material, course))

    return redirect(url_for('course_material_page', course=course, material=material), 302)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    session["id"] = None
    return redirect("/")


@app.route("/login", methods=["POST"])
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


@app.route("/courses/<course>/join", strict_slashes=False, methods=['POST'])
@requireLogin()
# Only students can join via this route
@requireRole(Role.student)
def join_course_student(course):
    # Validate course parameter
    try:
        course = getCourse(course_id=int(course))
        if course == None:
            raise ValueError()
    except:
        return "Error does not exist", 404

    # Course requires a password
    if course.mode == 2:
        if (request.form.get("course_password") != None) and (request.form.get("course_password") == course.code):
            course.add_member(g.user.id, Course.student)
    # All other cases
    else:
        course.add_member(g.user.id, Course.student)

    return redirect(url_for('course_page', course=course.id))


@app.route("/edit/courses/<course>/join", strict_slashes=False, methods=['POST'])
@requireLogin()
# Only coteachers can join via this route
@requireRole(Role.teacher)
def join_course_teacher(course):
    # Validate course parameter
    try:
        course = getCourse(course_id=int(course))
        if course == None:
            raise ValueError()
    except:
        return "Error does not exist", 404

    # Not considering other teachers to be possible attackers/threats
    course.add_member(g.user.id, Course.coteacher)

    return redirect(url_for('course_page', course=course.id))
