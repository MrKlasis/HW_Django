from abc import ABC, abstractmethod
import requests
import os

from requests import Response

from src.connector import Connector


class Engine(ABC):
    @abstractmethod
    def get_request(self) -> Response:
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    def __init__(self, keyword, page=0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": keyword,
            "page": page,
            "per_page": 100,
            "search_field": "name",
        }

    def get_request(self):
        try:
            request = requests.get(self.url, params=self.params)
        except requests.exception.RequestException as e:
            raise Exception
        else:
            return request


class Superjob(Engine):
    def __init__(self, keyword, page=1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {
            "keywords[0][keys]": keyword,
            "keywords[0][srws]": 4,
            "keywords[0][skwc]": "or",
            "page": page,
            "count": 100
        }

    def get_request(self):
        headers = {"X-Api-App-Id": os.environ["SUPERJOB_API_KEY"]}
        return requests.get(self.url, headers=headers, params=self.params)
