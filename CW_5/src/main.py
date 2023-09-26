from dbmanager import DBManager

def create_table(db_manager, table_name):
    conn = db_manager.connect()
    cursor = conn.cursor()

    query = f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, company VARCHAR(255), title VARCHAR(255), salary VARCHAR(255), link VARCHAR(255))"
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()


def main():
    db_manager = DBManager("CW_5", "080475", "5432")
    table_name = "CW_5"

    create_table(db_manager, table_name)

    # Получение списка всех компаний и количества вакансий
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    db_manager.insert_data(table_name, companies_and_vacancies)

    # Получение списка всех вакансий
    all_vacancies = db_manager.get_all_vacancies()
    db_manager.insert_data(table_name, all_vacancies)

    # Получение средней зарплаты по вакансиям
    avg_salary = db_manager.get_avg_salary()
    print("Average Salary:", avg_salary)

    # Получение списка вакансий с зарплатой выше средней
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print("High Salary Vacancies:")
    for vacancy in high_salary_vacancies:
        print(vacancy)

    # Получение списка вакансий с ключевым словом "python"
    keyword_vacancies = db_manager.get_vacancies_with_keyword("python")
    print("Keyword Vacancies:")
    for vacancy in keyword_vacancies:
        print(vacancy)

    # Извлечение данных из таблицы
    extracted_data = db_manager.select_data(table_name)
    print("Extracted Data:")
    for data in extracted_data:
        print(data)

if __name__ == "__main__":
    main()
