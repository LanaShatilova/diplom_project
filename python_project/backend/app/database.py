from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

# создание движка для взаимодействия с БД
# ORM - мы пишем классы (модели), пайтон их переводит в SQL-запросы
# echo=True - выводит полученные запросы после перевода
engine = create_engine(settings.database_url, echo=True)

# создание сессий (подключений) к БД
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# по правилам SQLalchemy все модели должны наследоваться от Base
# при этом он может быть и пустым
class Base(DeclarativeBase):
    pass

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    class_id INT NULL
);

CREATE TABLE Subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE Questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(20) NOT NULL CHECK (type IN ('one_ans', 'some_ans', 'correl', 'brief')),
    text TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE Tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sub_id INT NOT NULL,
    FOREIGN KEY (sub_id) REFERENCES Subjects(id) ON DELETE CASCADE
);

CREATE TABLE Assigned (
    id INT PRIMARY KEY AUTO_INCREMENT,
    q_id INT NOT NULL,
    t_id INT NOT NULL,
    FOREIGN KEY (q_id) REFERENCES Questions(id) ON DELETE CASCADE,
    FOREIGN KEY (t_id) REFERENCES Tests(id) ON DELETE CASCADE,
    UNIQUE (q_id, t_id)
);

CREATE TABLE Exams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    teacher_id INT NOT NULL,
    student_id INT NOT NULL,
    FOREIGN KEY (test_id) REFERENCES Tests(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE
);

INSERT INTO Subjects (name) VALUES ('Математика'), ('Русский язык'), ('Окружающий мир'), ('Английский язык'), ('Литературное чтение');

INSERT INTO Tests (sub_id) VALUES (1), (1);
INSERT INTO Questions (type, text, answer) VALUES
('one_ans', 'Вычисли: 53+28', '81'),
('one_ans', 'Вычисли: 26-6*3+29', '37'),
('one_ans', 'Во сколько начались занятия спортивной секции, если они длились 1 час 30 минут и закончились в 17 часов 15 минут?', '15часов 45 минут')
('one_ans', 'Найди значение выражения: 12012:3-170*4', '3324'),
('one_ans', 'Три килограмма варенья разложили в банки по 400г и в банки по 200г.Банок по 400г получилось 4. Сколько потребовалось банок по 200г?', '7')
('one_ans', 'В магазине продавали трехколесные и двухколесные велосипеды. Максим персчитал все рули и все колеса. Получилось 12 рулей и 27 колёс. Сколько трёхколёсных велосипедов продавали в магазине?', '3')
('one_ans', 'Вычисли: 7+3*(8+12)', '67');



