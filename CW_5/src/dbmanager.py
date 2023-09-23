import psycopg2
import requests


def get_all_vacancies():
    url = "https://api.hh.ru/vacancies"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies = []

        for vacancy in data["items"]:
            company_name = vacancy["employer"]["name"]
            vacancy_title = vacancy["name"]
            salary = vacancy["salary"]
            vacancy_link = vacancy["alternate_url"]

            if salary is not None:
                salary_text = f"{salary['from']} - {salary['to']} {salary['currency']}"
            else:
                salary_text = "Не указана"

            vacancies.append({
                "Компания": company_name,
                "Вакансия": vacancy_title,
                "Зарплата": salary_text,
                "Ссылка": vacancy_link
            })

        return vacancies
    else:
        print("Ошибка при получении данных. Код ошибки:", response.status_code)
        return None


class DBManager:

    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> None:
        '''
        Инициализация класса DBManager
        :param db_name:
        :param db_user:
        :param db_password:
        :param db_host:
        :param db_port:
        '''
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.connection = psycopg2.connect(dbname='postgres',
                                           user=self.db_user,
                                           password=self.db_password,
                                           host=self.db_host,
                                           port=db_port)

    def create_database(self):
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="080475"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE job_data")
        cursor.close()
        conn.close()

    def create_tables(self):
        conn = psycopg2.connect(
            host="your_host",
            port="your_port",
            user="your_user",
            password="your_password",
            database="job_data"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                vacancies_count INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER,
                name VARCHAR(255),
                salary VARCHAR(255),
                link VARCHAR(255),
                FOREIGN KEY (employer_id) REFERENCES employers (id)
            )
        """)
        cursor.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        url = "https://api.hh.ru/employers/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            companies = []

            for employer in data:
                company_name = employer["name"]
                vacancies_count = employer["vacancies_count"]
                companies.append((company_name, vacancies_count))

            return companies
        else:
            print("Ошибка при получении данных. Код ошибки:", response.status_code)
            return None

    def get_avg_salary(self):
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            salaries = []

            for vacancy in data["items"]:
                salary = vacancy["salary"]

                if salary is not None:
                    if salary["currency"] == "RUR":
                        if salary["from"] is not None and salary["to"] is not None:
                            avg_salary = (salary["from"] + salary["to"]) / 2
                        elif salary["from"] is not None:
                            avg_salary = salary["from"]
                        elif salary["to"] is not None:
                            avg_salary = salary["to"]
                        else:
                            continue  # Пропускаем вакансии без указания зарплаты
                        salaries.append(avg_salary)

            if len(salaries) > 0:
                avg_salary = sum(salaries) / len(salaries)
                return avg_salary
            else:
                return None
        else:
            print("Ошибка при получении данных. Код ошибки:", response.status_code)
            return None

    def get_vacancies_with_higher_salary(self):
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            salaries = []
            vacancies = []

            for vacancy in data["items"]:
                salary = vacancy["salary"]

                if salary is not None:
                    if salary["currency"] == "RUR":
                        if salary["from"] is not None and salary["to"] is not None:
                            avg_salary = (salary["from"] + salary["to"]) / 2
                        elif salary["from"] is not None:
                            avg_salary = salary["from"]
                        elif salary["to"] is not None:
                            avg_salary = salary["to"]
                        else:
                            continue  # Пропускаем вакансии без указания зарплаты
                        salaries.append(avg_salary)
                        vacancies.append(vacancy)

            if len(salaries) > 0:
                avg_salary = sum(salaries) / len(salaries)
                high_salary_vacancies = [vacancy for vacancy in vacancies if
                                         vacancy["salary"] is not None and vacancy["salary"]["currency"] == "RUR" and
                                         vacancy["salary"]["to"] is not None and vacancy["salary"]["to"] > avg_salary]
                return high_salary_vacancies
            else:
                return None
        else:
            print("Ошибка при получении данных. Код ошибки:", response.status_code)
            return None

    def get_vacancies_with_keyword(self, keyword):
        url = f"https://api.hh.ru/vacancies?text={keyword}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            vacancies = data["items"]

            if len(vacancies) > 0:
                return vacancies
            else:
                return None
        else:
            print("Ошибка при получении данных. Код ошибки:", response.status_code)
            return None
