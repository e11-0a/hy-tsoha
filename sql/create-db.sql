CREATE TABLE users (
    id                  SERIAL PRIMARY KEY,
    username            text UNIQUE NOT NULL,
    chosen_name         text,
    password            text NOT NULL,
    created             int,
    modified            int,
    active              boolean NOT NULL,
    source              integer NOT NULL,
    comment             text
);

CREATE TABLE roles (
    id                  SERIAL PRIMARY KEY,
    name                text NOT NULL,
    description         text
);

INSERT INTO roles (name, description) VALUES (
    'teacher', 'teacher role'
);

INSERT INTO roles (name, description) VALUES (
    'student', 'student role'
);

INSERT INTO roles (name, description) VALUES (
    'superuser', 'superuser role'
);

CREATE TABLE userRoles (
    id                  SERIAL PRIMARY KEY,
    user_id             INT NOT NULL,
    role_id             INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_role FOREIGN KEY(role_id) REFERENCES roles(id)  
);

CREATE TABLE courses (
    id                  SERIAL PRIMARY KEY,
    codename            text NOT NULL,
    title               text,
    description         text,
    -- 0=public, 1=require join, 2=require code
    mode                int NOT NULL,
    code                text,
    created             int,
    modified            int
);

CREATE TABLE courseMembers (
    id                  SERIAL PRIMARY KEY,
    user_id             INT NOT NULL,
    course_id           INT NOT NULL,
    user_type           INT NOT NULL,
    -- 0 = student, 1 = owner, 2 = co-teacher
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_course FOREIGN KEY(course_id) REFERENCES courses(id)  
);

CREATE TABLE courseMaterials (
    id                  SERIAL PRIMARY KEY,
    course_id           INT NOT NULL,
    material_type       INT NOT NULL,
    -- 0 = text/material, 1 = exercise, 2 = file
    content             text,
    -- (isojen) Tiedostojen säilytys tietokannassa on huono idea, mutta
    -- maks muutaman kb:n tiedostot ei varmaa tuhoa koko kantaa
    -- https://stackoverflow.com/a/9606063
    name                text,
    description         text,
    CONSTRAINT fk_course FOREIGN KEY(course_id) REFERENCES courses(id)  
);

