from db import connection_pool
import json

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

class Exercise:
    def __init__(self, exerciseSource: dict) -> None:
        self.source = exerciseSource
        self.automatic = True
        self.validateSource()
        self.type = self.source["type"]
    
    def validateSource(self):
        try:
            if self.source["type"] in ["multiple_choice", "short_text_answer", "freetext"]:
                if self.source["type"] == "freetext":
                    self.automatic = False
                    if "question" not in self.source:
                        raise ValueError("No question provided for freetext")
                if self.source["type"] == "multiple_choice":
                    if "question" not in self.source:
                        raise ValueError("No question provided for multiple_choice")
                    if "answers" not in self.source:
                        raise ValueError("No answers provided for multiple_choice")
                    if len(self.source["answers"]) < 2:
                        raise ValueError("Not enough answers provided for multiple_choice")
                    for i in self.source["answers"]:
                        if "text" not in i:
                            raise ValueError("No text in answer")
                        if "id" not in i:
                            raise ValueError("No id in answer")
                        if "points" not in i:
                            raise ValueError("No points in answer")
                if self.source["type"] == "short_text_answer":
                    if "question" not in self.source:
                        raise ValueError("No question provided for short_text_answer")
                    if "answers" not in self.source:
                        raise ValueError("No answers provided for short_text_answer")
                    if len(self.source["answers"]) < 1:
                        raise ValueError("Not enough answers provided for short_text_answer")
                    for i in self.source["answers"]:
                        if "text" not in i:
                            raise ValueError("No text in answer")
                        if "points" not in i:
                            raise ValueError("No points in answer")
                
        except Exception as e:
            raise ValueError("Exercise validation failed", e)
    
    def grade(self, answer: str|int):
        # answer format
        # id|"text"

        if self.type == "freetext":
            return {"value":None, "message":"Vapaatekstikenttiä ei konearvioida"}
        elif self.type == "multiple_choice":
            possible = list(map(lambda x: x["id"], self.source["answers"]))
            if answer in possible:
                result = self.source["answers"][possible.index(answer)]
                return {"value":result["points"], "message":None}
            else:
                raise ValueError("Invalid answer")
        elif self.type == "short_text_answer":
            possible = list(map(lambda x: x["text"], self.source["answers"]))
            if answer in possible:
                result = self.source["answers"][possible.index(answer)]
                return {"value":result["points"], "message":None}
            else:
                return {"value":0, "message":None}
        raise Exception("Cannot grade exercise")

    @property
    def readableType(self):
        return {
            "freetext":"Vapaa teksti",
            "multiple_choice": "Monivalinta",
            "short_text_answer":"Lyhyt teksti"
        }[self.type]
    
    @property
    def question(self):
        return self.source["question"]
    
    @property
    def answers(self):
        return self.source["answers"]

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
    
    def get_exercises(self) -> dict:
        if self.type == 1:
            content = json.loads(self.content)
            return list(map(lambda x: Exercise(x), content["exercises"]))

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
    # TODO: inline this
    @property
    def name(self):
        if self.chosen_name != None:
            return self.chosen_name
        return self.username
    
    def get_named_roles(self):
        return list(map(lambda x: ["Opettaja", "Opiskelija", "Pääkäyttäjä"][x-1], self.roles))

    def has_role(self, role: int) -> bool:
        return role in self.roles