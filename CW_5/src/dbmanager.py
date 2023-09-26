import requests
import psycopg2

class DBManager:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def get_companies_and_vacancies_count(self):
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)
        data = response.json()

        companies = {}
        for vacancy in data['items']:
            company = vacancy['employer']['name']
            if company in companies:
                companies[company] += 1
            else:
                companies[company] = 1

        return companies

    def get_all_vacancies(self):
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)
        data = response.json()

        vacancies = []
        for vacancy in data['items']:
            company = vacancy['employer']['name']
            title = vacancy['name']
            salary = vacancy['salary']
            link = vacancy['alternate_url']
            vacancies.append({
                'company': company,
                'title': title,
                'salary': salary,
                'link': link
            })

        return vacancies

    def get_avg_salary(self):
        vacancies = self.get_all_vacancies()
        total_salary = 0
        count = 0

        for vacancy in vacancies:
            salary = vacancy['salary']
            if salary and salary['currency'] == 'RUR':
                if salary['from']:
                    total_salary += salary['from']
                    count += 1
                if salary['to']:
                    total_salary += salary['to']
                    count += 1

        if count > 0:
            avg_salary = total_salary / count
            return avg_salary
        else:
            return None

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        vacancies = self.get_all_vacancies()
        high_salary_vacancies = []

        for vacancy in vacancies:
            salary = vacancy['salary']
            if salary and salary['currency'] == 'RUR':
                if salary['from'] and salary['from'] > avg_salary:
                    high_salary_vacancies.append(vacancy)
                if salary['to'] and salary['to'] > avg_salary:
                    high_salary_vacancies.append(vacancy)

        return high_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        vacancies = self.get_all_vacancies()
        keyword_vacancies = []

        for vacancy in vacancies:
            title = vacancy['title']
            if keyword.lower() in title.lower():
                keyword_vacancies.append(vacancy)

        return keyword_vacancies

    def insert_data(self, table_name, data):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        cursor = conn.cursor()

        for vacancy in data:
            company = vacancy['company']
            title = vacancy['title']
            salary = vacancy['salary']
            link = vacancy['link']
            query = f"INSERT INTO {table_name} (company, title, salary, link) VALUES ('{company}', '{title}', '{salary}', '{link}')"
            cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def select_data(self, table_name):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data
