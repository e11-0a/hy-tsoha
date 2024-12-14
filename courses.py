from flask import render_template, request, redirect, g, url_for

from app import app
from db import connection_pool
from model import *
from utils import *


@app.route("/courses", strict_slashes=False)
@requireLogin()
def course_index():
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_list: list[Course] = list(map(lambda x: Course(x[0], x[1], x[2], x[3], x[4], code=x[5], created=x[6], modified=[7]), cur.execute(
            "SELECT id, codename, title, description, mode, code, created, modified FROM courses").fetchall()))
    return render_template("courses.jinja", user=g.user, courses=course_list, role=Role)


@app.route("/courses/<course>", strict_slashes=False)
@verifyCourseAccess()
def course_page(course):
    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))
    return render_template("course.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=None, role=Role)


@app.route("/courses/<course>/overview", strict_slashes=False)
@requireLogin()
@verifyCourseAccess()
def course_overview(course):

    with connection_pool.connection() as conn:
        cur = conn.cursor()
        course_materials: list[Material] = list(map(lambda x: Material(x[0], g.course.id, x[1], x[2]), cur.execute(
            'SELECT id, name, material_type FROM courseMaterials WHERE course_id=%s', (g.course.id,)).fetchall()))
        done_exercises = None
        if g.user.has_role(Role.student):
            done_exercises = cur.execute(
                'SELECT DISTINCT ON (g.material_id, g.exercise_id, g.user_id)g.id, g.user_id, u.chosen_name, g.material_id, g.exercise_id, g.points, g.comment FROM gradedExercises g LEFT JOIN users u ON u.id=g.user_id WHERE g.course_id=%s AND g.user_id=%s ORDER BY g.material_id ASC, g.exercise_id ASC, g.user_id ASC, g.id DESC ', (g.course.id, g.user.id)).fetchall()
        elif g.user.has_role(Role.teacher):
            done_exercises = cur.execute(
                'SELECT DISTINCT ON (g.material_id, g.exercise_id, g.user_id)g.id, g.user_id, u.chosen_name, g.material_id, g.exercise_id, g.points, g.comment FROM gradedExercises g LEFT JOIN users u ON u.id=g.user_id WHERE g.course_id=%s ORDER BY g.material_id ASC, g.exercise_id ASC, g.user_id ASC, g.id DESC ', (g.course.id,)).fetchall()


    return render_template("overview.jinja", user=g.user, course=g.course, course_materials=course_materials, done_exercises=done_exercises, role=Role, current_material=None)


@app.route("/courses/<course>/<material>", strict_slashes=False)
@verifyCourseAccess()
def course_material_page(course, material):

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

        if g.user:
            db_past_answers = cur.execute(
                'SELECT id, exercise_id, points, comment FROM gradedExercises WHERE course_id=%s AND material_id=%s AND user_id=%s ORDER BY id DESC', (g.course.id, material, g.user.id)).fetchall()

            past_answers = {}
        else:
            db_past_answers = None
        if db_past_answers == None:
            past_answers = None
        else:
            for i in db_past_answers:
                if i[1] in past_answers:
                    past_answers[i[1]].append(i)
                else:
                    past_answers[i[1]] = [i]


        # Loaded as necessary, so not populated by default
        current_material.name = db_current_material[1]
        current_material.type = int(db_current_material[2])
        current_material.content = db_current_material[3]

    return render_template("course.jinja", user=g.user, course=g.course, course_materials=course_materials, current_material=current_material, past_answers=past_answers, role=Role)


@app.route("/courses/<course>/<material>", strict_slashes=False, methods=["POST"])
@requireOrigin()
@requireRole(Role.student)
@verifyCourseAccess()
def grade_answers(course, material):
    try:
        current_material = Material(int(material), g.course.id)
    except ValueError:
        return render_template("error.jinja", error_title="Material does not exist", error_body="Invalid material ID"), 404
    with connection_pool.connection() as conn:
        cur = conn.cursor()

        db_current_material = cur.execute(
            'SELECT material_type, content FROM courseMaterials WHERE course_id=%s AND id=%s', (g.course.id, material)).fetchone()

        if db_current_material == None:
            return render_template("error.jinja", error_title="Material does not exist", error_body="Material with provided ID does not exist in the course"), 404

        current_material.content = db_current_material[1]
        current_material.type = db_current_material[0]

        questions = current_material.get_exercises()
        answers = request.form

        if questions == None:
            return render_template("error.jinja", error_title="Kohde ei ole tehtävä", error_body="Ei voida suorittaa arvostelua, koska kohde ei ole tehtävä"), 404


        graded_answers = []

        for i in answers:
            try:
                question_id = int(i)-1
            except ValueError:
                return render_template("error.jinja", error_title="Epäkelpo vastaus", error_body="Tuntematon tehtävä"), 404
            if question_id > len(questions):
                return render_template("error.jinja", error_title="Epäkelpo vastaus", error_body="Liian monta vastausta tehtävään"), 404

            question = questions[question_id]
            answer = answers[i]
            if question.type == "multiple_choice":
                answer = int(answer)
            graded = question.grade(answer)
            graded["exercise_id"] = question_id
            graded_answers.append(graded)


        grades = []

        for item in graded_answers:
            grades.append(
                (g.course.id, material, item["exercise_id"], g.user.id, item["value"], item["message"]))

        cur.executemany(
            "INSERT INTO gradedExercises (course_id, material_id, exercise_id, user_id, points, comment) VALUES (%s, %s, %s, %s, %s, %s)", grades)

    # return graded_answers

    return redirect(url_for("course_material_page", course=g.course.id, material=material))


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
