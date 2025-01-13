class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(
        self,
        name: str,
        url: str,
        salary: int | None,
        responsibility: str | None,
    ) -> None:
        self.__name = name
        self.__url = url
        self.__salary = self.__validate_salary(salary)
        self.__responsibility = self.__validate_responsibility(responsibility)

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def responsibility(self):
        return self.__responsibility

    @classmethod
    def __validate_salary(cls, salary: int | None) -> int:
        return salary or 0

    @classmethod
    def __validate_responsibility(cls, responsibility: str | None) -> str:
        return responsibility or ""

    # def __str__(self):
    #     lines = [
    #         f"Название вакансии: {self.__name}",
    #         f"Ссылка на вакансия: {self.__url}",
    #         f"Зарплата от: {self.__salary_from}",
    #         f"Зарплата до: {self.__salary_to}",
    #         f"Валюта: {self.__currency}",
    #         f"Описание вакансий: {self.__responsibility}",
    #     ]
    #     return "\n".join(lines)

    @classmethod
    def create_from_dict(cls, data: dict):
        """Создает вакансию из словаря полученного из HH"""
        name = str(data.get("name"))
        url = str(data.get("alternate_url"))
        salary_dict = data.get("salary") or {}
        salary = max(salary_dict.get("to") or 0, salary_dict.get("from") or 0)
        snippet_dict = data.get("snippet") or {}
        responsibility = snippet_dict.get("responsibility")

        return cls(name, url, salary, responsibility)

    @classmethod
    def cast_to_object_list(cls, data: list[dict]) -> list["Vacancy"]:
        """Создает список вакансий из списка словарей HH"""
        list_vacancy = []
        for vacancy_dict in data:
            list_vacancy.append(cls.create_from_dict(vacancy_dict))

        return list_vacancy
