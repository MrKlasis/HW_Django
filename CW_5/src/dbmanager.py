import psycopg2

class DBManager:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

    def get_companies_and_vacancies_count(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """)
        return cur.fetchall()

    def get_all_vacancies(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """)
        return cur.fetchall()

    def get_avg_salary(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG(salary_min + salary_max) / 2
            FROM vacancies;
        """)
        return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE (vacancies.salary_min + vacancies.salary_max) / 2 > %s;
        """, (avg_salary,))
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.name ILIKE %s;
        """, ('%' + keyword + '%',))
        return cur.fetchall()

