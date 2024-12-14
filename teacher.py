from flask import render_template, request, session, redirect, g, url_for
from functools import wraps
from argon2.exceptions import VerificationError

from app import app
from db import connection_pool
from model import *
import hashing
import time
from utils import *
import json

@app.route("/edit/courses/new", strict_slashes=False, methods=['GET'])
@requireRole(Role.teacher)
def new_course():
    return render_template('new_course.jinja', user=g.user, role=Role)


@app.route("/edit/courses/new", strict_slashes=False, methods=['POST'])
@requireOrigin()
@requireRole(Role.teacher)
def create_course():

    course_name = str(request.form["name"])
    course_code = str(request.form["code"])
    course_desc = str(request.form["desc"])
    course_type = str(request.form["type"])
    course_key = str(request.form["key"])

    if len(course_name) < 1:
        return render_template("error.jinja", error_title="Epäkelpo nimi", error_body="Kurssin nimi ei voi olla tyhjä"), 400

    if len(course_code) < 1:
        return render_template("error.jinja", error_title="Epäkelpo kurssikoodi", error_body="Kurssin koodi ei voi olla tyhjä"), 400

    if not (course_type in ["open", "join", "code"]):
        return render_template("error.jinja", error_title="Epäkelpo kurssityyppi", error_body="Kurssityyppi ei käytettävissä"), 400
    else:
        course_type = {
            "open": 0,
            "join": 1,
            "code": 2
        }[course_type]

    if (course_type == 3) and (len(course_key) < 1):
        return render_template("error.jinja", error_title="Epäkelpo avainkoodi", error_body="Avainkoodi ei saa olla tyhjä kurssityypin ollessa \"Vaatii koodin\""), 400

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO courses (codename, title, description, mode, created, modified) VALUES (
                        %s, %s,%s,%s,%s,%s
                    ) RETURNING id;''', (course_code, course_name, course_desc, course_type, int(time.time()), int(time.time())))
        course_id = cur.fetchone()[0]
        cur.execute(
            '''INSERT INTO courseMembers (user_id, course_id, user_type) VALUES (%s, %s, 0);''', (g.user.id, course_id))
        return redirect(url_for('course_page', course=course_id), 302)
    return render_template("error.jinja", error_title="Tuntematon virhe", error_body="Kurssia luodessa tapahtui tuntematon virhe"), 500


@app.route("/edit/courses/<course>/<material>", strict_slashes=False)
@verifyCourseAccess()
@requireRole(Role.teacher)
def course_material_edit(course, material):
    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Material does not exist", error_body="Invalid material ID"), 404

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))

        db_current_material = cur.execute(
            'SELECT id, name, material_type, content FROM courseMaterials WHERE course_id=%s AND id=%s', (g.course.id, material)).fetchone()

        if db_current_material == None:
            return render_template("error.jinja", error_title="Material does not exist", error_body="Material with provided ID does not exist in the course"), 404

        # Loaded as necessary, so not populated by default
        current_material.name = db_current_material[1]
        current_material.type = int(db_current_material[2])
        current_material.content = db_current_material[3]
    return render_template("course_editor.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=current_material, role=Role)

# Save material edits


@app.route("/edit/courses/<course>/<material>", strict_slashes=False, methods=['POST'])
@requireOrigin()
@verifyCourseAccess()
@requireRole(Role.teacher)
def save_course_material(course, material):


    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Invalid material", error_body="Invalid material ID"), 404

    text = request.form["editor"]
    # TODO: solve flask's POST max size

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        material_type = cur.execute(
            'SELECT material_type FROM courseMaterials WHERE id=%s AND course_id=%s', (material, course)).fetchone()
        if material_type == None:
            return render_template("error.jinja", error_title="Materiaalia ei löydy", error_body="Muokattavaa materiaalia ei löydy"), 404
        elif material_type[0] == 1:
            try:
                test = list(map(lambda x: Exercise(x), json.loads(text)["exercises"]))
            except Exception as e:
                return render_template("error.jinja", error_title="Tehtävän validointi epäonnistui", error_body=f"Validaattori antoi seuraavan virheen: {e}"), 404


        cur.execute(
            'UPDATE courseMaterials SET content=%s WHERE id=%s AND course_id=%s', (text, material, course))

    return redirect(url_for('course_material_page', course=course, material=material), 302)


@app.route("/edit/courses/<course>/new", strict_slashes=False, methods=['GET'])
@verifyCourseAccess()
@requireRole(Role.teacher)
def new_course_material(course):
    return render_template('new_material.jinja', user=g.user, course=g.course, role=Role)


@app.route("/edit/courses/<course>/new", strict_slashes=False, methods=['POST'])
@requireOrigin()
@verifyCourseAccess()
@requireRole(Role.teacher)
def create_course_material(course):

    material_name = str(request.form["name"])
    material_type = str(request.form["type"])

    if len(material_name) < 1:
        return render_template("error.jinja", error_title="Epäkelpo materiaalin nimi", error_body="Materiaalin nimi ei voi olla tyhjä"), 400

    if not (material_type in ["exercise", "material"]):
        return render_template("error.jinja", error_title="Epäkelpo materialityyppi", error_body="Materiaalityyppi ei käytettävissä"), 400
    else:
        material_type = {
            "material": 0,
            "exercise": 1,
        }[material_type]

    # TODO: solve flask's POST max size

    templates = {
        0: "<i>Empty material</i>",
        1: "{\"exercises\":[]}"
    }

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO courseMaterials (course_id, material_type, content, name) VALUES (
                            %s,
                            %s,
                            %s,
                            %s
                      ) RETURNING id;''', (course,
                                           material_type,
                                           templates[material_type],
                                           material_name))
        id_of_new_row = cur.fetchone()[0]
    return redirect(url_for('course_material_page', course=course, material=id_of_new_row), 302)


@app.route("/edit/courses/<course>/join", strict_slashes=False, methods=['POST'])
@requireLogin()
@requireOrigin()
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
