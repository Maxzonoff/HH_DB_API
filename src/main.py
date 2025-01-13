from src.DB_creater import create_db, fill_vacancies
from src.head_hunter import HeadHunter


def main():
    create_db()
    fill_vacancies()
    print("Введите номер действия:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании.")
    print(
        """2. Получить список всех вакансий с указанием названия компании,
    названия вакансии и зарплаты и ссылки на вакансию."""
    )
    print("3. Получить среднюю зарплату по вакансиям.")
    print(
        "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям."
    )
    print(
        "5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова."
    )
    user = int(input())
    hh = HeadHunter()
    if user == 1:
        hh.employers_and_vacancies_count()
    if user == 2:
        hh.all_vacancies()
    if user == 3:
        hh.avg_salary()
    if user == 4:
        hh.vacancies_with_higher_salary()
    if user == 5:
        word = input()
        hh.vacancies_with_keyword(word)


if __name__ == "__main__":
    main()
