from db import connection_pool

class Role:
    teacher = 1
    student = 2
    superuser = 3

class Course:
    teacher = 1
    coteacher = 2
    student = 0

    def __init__(self, course_id: int, codename: str, title: str, description: str, mode: int, code=None, created=None, modified=None) -> None:
        self.id = course_id
        self.codename = codename
        self.title = title
        self.description = description
        self.mode = mode
        self.created = created
        self.modified = modified
        self.code = code

    # Make human-readable
    @property
    def mode_text(self):
        return ["Avoin", "Vaatii liittymisen", "Vaatii koodin"][self.mode]

    def isMember(self, user_id) -> bool:
        with connection_pool.connection() as conn:
            cur = conn.cursor()
            db_course = cur.execute(
                "SELECT id FROM courseMembers WHERE user_id=%s AND course_id=%s", (user_id, self.id)).fetchone()
        return db_course != None

    def add_member(self, user_id: int, user_type: int):
        with connection_pool.connection() as conn:
            cur = conn.cursor()
            db_course = cur.execute(
                "INSERT INTO courseMembers (user_id, course_id, user_type) VALUES (%s, %s, %s)", (user_id, self.id, user_type))

class Material:
    def __init__(self, material_id, course_id, name=None, material_type=None, content=None, description=None) -> None:
        self.id = material_id
        self.course_id = course_id
        self.name = name
        self.type = material_type
        self.content = content
        self.description = description

    # Human readable names
    @property
    def type_string(self) -> str:
        if self.type != None:
            return ['Aineisto', 'Tehtävä', 'Tiedosto'][self.type]
        return "Tuntematon"

class User:
    def __init__(self, user_id, username, active, chosen_name=None, created=None, modified=None, source=None, comment=None, roles=[]) -> None:
        self.id = user_id
        self.username = username
        self.chosen_name = chosen_name
        self.created = created
        self.modified = modified
        self.active = active
        self.source = source
        self.comment = comment
        self.roles = roles

    # Handle getting users name
    @property
    def name(self):
        if self.chosen_name != None:
            return self.chosen_name
        return self.username

    def has_role(self, role: int) -> bool:
        return role in self.roles