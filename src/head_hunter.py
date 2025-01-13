from src.DB_Manager import DBManager


class HeadHunter:
    def __init__(self):
        self.__db_manager = DBManager()

    def employers_and_vacancies_count(self) -> None:
        rows = self.__db_manager.get_companies_and_vacancies_count()
        for row in rows:
            print(f"Компания: {row[0]}, Количество вакансий: {row[1]}")

    def all_vacancies(self):
        rows = self.__db_manager.get_all_vacancies()
        for row in rows:
            print(f"Название вакансии: {row[0]}")
            print(f"Ссылка на вакансию: {row[1]}")
            print(f"Зарплата: {row[2]}")
            print(f"Компания: {row[3]}")
            print()

    def avg_salary(self):
        avg = self.__db_manager.get_avg_salary()
        print(f"Средняя зарплата: {avg}")

    def vacancies_with_higher_salary(self):
        rows = self.__db_manager.get_vacancies_with_higher_salary()
        for row in rows:
            print(row)

    def vacancies_with_keyword(self, word: str):
        rows = self.__db_manager.get_vacancies_with_keyword(word)
        for row in rows:
            print(f"Название вакансии: {row[1]}")
            print(f"Ссылка на вакансию: {row[2]}")
            print(f"Зарплата: {row[3]}")
            print(f"Описание: {row[4]}")
            print()
