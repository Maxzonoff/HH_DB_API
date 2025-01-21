import os

import psycopg2
from dotenv import load_dotenv

from src.vacancy import Vacancy

load_dotenv()


class DBManager:
    """Клас для взаимодействия с базой данных."""
    def __init__(self):
        self.conn_params = dict(
            host=os.getenv("DATABASE_HOST"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT EMPLOYERS.NAME, COUNT(VACANCIES.EMPLOYER_ID)
                    FROM EMPLOYERS
                    LEFT JOIN VACANCIES ON EMPLOYERS.EMPLOYER_ID=VACANCIES.EMPLOYER_ID
                    GROUP BY EMPLOYERS.NAME"""
                )
                return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT vacancies.name, vacancies.url, vacancies.salary, employers.name
                FROM vacancies
                LEFT JOIN employers USING(employer_id);"""
                )
                return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT AVG(salary) FROM vacancies WHERE salary > 0;""")
                return round(cur.fetchall()[0][0], 2)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VACANCIES
                    WHERE SALARY > (SELECT AVG(SALARY) FROM VACANCIES)
                """
                )
                return cur.fetchall()

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT *
                    FROM VACANCIES
                    WHERE lower(responsibility) like '%{word.lower()}%'
                """
                )
                return cur.fetchall()

    def insert_vacancy(self, vacancy: Vacancy, employer_id) -> None:
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO public.vacancies(
                    name, url, salary, responsibility, employer_id)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (
                        vacancy.name,
                        vacancy.url,
                        vacancy.salary,
                        vacancy.responsibility,
                        employer_id,
                    ),
                )

    def get_employers(self):
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                    EMPLOYER_ID,
                    HH_ID,
                    NAME
                FROM
                    EMPLOYERS
                    """
                )
                return cur.fetchall()
