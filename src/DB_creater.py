import os

import psycopg2
from dotenv import load_dotenv

from src.DB_Manager import DBManager
from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy

load_dotenv()

conn_params = dict(
    host=os.getenv("DATABASE_HOST"),
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
)


def create_employers():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employers
                    (
                    employer_id serial PRIMARY KEY,
                    hh_id INT,
                    name VARCHAR(100)
                    )"""
            )


def create_vacancies():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE vacancies
                (
                vacancy_id serial PRIMARY KEY,
                name VARCHAR,
                url VARCHAR,
                salary int,
                responsibility text,
                employer_id int REFERENCES employers (employer_id)
                );"""
            )


def drop_tables():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """DROP TABLE IF EXISTS vacancies, employers;
"""
            )


def fill_employers():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO public.employers(
                employer_id, hh_id, name)
                VALUES
                (1, 15478, 'VK'),
                (2, 1740, 'яндекс'),
                (3, 78638, 'т-банк'),
                (4, 3529, 'сбер'),
                (5, 2180, 'OZON'),
                (6, 3776, 'МТС'),
                (7, 3127, 'МЕГАФОН'),
                (8, 4934, 'Билайн'),
                (9, 3388, 'Газпромбанк'),
                (10, 1455, 'HeadHunter')"""
            )


def fill_vacancies():
    db = DBManager()
    employers = db.get_employers()
    hh = HeadHunterAPI()
    for employer in employers:
        employer_id = employer[0]
        employer_hh_id = employer[1]
        hh.get_vacancies(str(employer_hh_id))
        vacancies = Vacancy.cast_to_object_list(hh.vacancies)
        for vac in vacancies:
            db.insert_vacancy(vac, employer_id)
        print(employer)


def create_db():
    drop_tables()
    create_employers()
    create_vacancies()
    fill_employers()
