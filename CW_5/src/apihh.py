import requests
import settings
import sqlite3


class ApiHH():
    def __init__(self):
        self.db_connection = sqlite3.connect(settings.DB_PATH)
        self.db_cursor = self.db_connection.cursor()

    def get_employees(self):
        employer_ids = [
            78638,  # Тинькофф
            1740,  # Яндекс
            3529,  # Сбербанк
        ]

        for employer_id in employer_ids:
            url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50'
            response = requests.get(url)
            print(response.json())

    def get_vacancies_by_company(self, employer_id):
        url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50'
        response = requests.get(url)

        if response.status_code == 200:
            vacancies_data = response.json()
            vacancies = vacancies_data.get("items", [])
        else:
            print(f"Ошибка при получении данных для компании с ID {employer_id}")
            vacancies = []

        return vacancies

    def save_to_database(self, data):
        # Здесь выполняется сохранение данных в базу данных
        # Пример:
        self.db_cursor.execute("INSERT INTO vacancies (data) VALUES (?)", (data,))
        self.db_connection.commit()


