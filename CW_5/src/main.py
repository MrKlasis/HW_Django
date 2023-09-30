from dbmanager import DBManager

def main():
    # Параметры подключения к базе данных PostgreSQL
    host = 'localhost'
    port = 5432
    database = 'CW_5'
    user = 'Smirnov'
    password = '080475'

    # Создание экземпляра класса DBManager
    db_manager = DBManager(host=host, port=port, database=database, user=user, password=password)

    # Создание таблицы vacancies, если она не существует
    create_table_query = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            salary_min INTEGER,
            salary_max INTEGER,
            url VARCHAR(255),
            company_id INTEGER
        );
    """
    cur = db_manager.conn.cursor()
    cur.execute(create_table_query)
    db_manager.conn.commit()

    # Пример использования функций класса DBManager
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    all_vacancies = db_manager.get_all_vacancies()
    avg_salary = db_manager.get_avg_salary()
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword('python')

    # Вывод результатов
    print("Список компаний и количество вакансий:")
    for company, vacancy_count in companies_and_vacancies:
        print(f"{company}: {vacancy_count}")

    print("\nСписок всех вакансий:")
    for company, vacancy, salary_min, salary_max, url in all_vacancies:
        print(f"Компания: {company}, Вакансия: {vacancy}, Зарплата: {salary_min}-{salary_max}, URL: {url}")

    print("\nСредняя зарплата по вакансиям:", avg_salary)

    print("\nСписок вакансий с зарплатой выше средней:")
    for company, vacancy, salary_min, salary_max, url in vacancies_with_higher_salary:
        print(f"Компания: {company}, Вакансия: {vacancy}, Зарплата: {salary_min}-{salary_max}, URL: {url}")

    print("\nСписок вакансий с ключевым словом 'python':")
    for company, vacancy, salary_min, salary_max, url in vacancies_with_keyword:
        print(f"Компания: {company}, Вакансия: {vacancy}, Зарплата: {salary_min}-{salary_max}, URL: {url}")

if __name__ == '__main__':
    main()
