import abc

import requests


class HeadHunterAPIBase(abc.ABC):
    """Базовый класс для взаимодействия c API HH"""

    @abc.abstractmethod
    def get_vacancies(self, keyword):
        pass


class HeadHunterAPI(HeadHunterAPIBase):
    """Класс для взаимодействия c API HH"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__vacancies: list[dict] = []

    @property
    def vacancies(self) -> list[dict]:
        return self.__vacancies

    def get_vacancies(self, employer_id: str) -> None:
        """Получение вакансии с hh.ru"""
        # https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies
        self.__vacancies = []
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__params["employer_id"] = employer_id
        while self.__params.get("page") != 20:
            response = self.__connect_to_api()
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

    def __connect_to_api(self):
        """Отправить запрос в HH API"""
        response = requests.get(
            self.__url, headers=self.__headers, params=self.__params
        )
        response.raise_for_status()
        return response
