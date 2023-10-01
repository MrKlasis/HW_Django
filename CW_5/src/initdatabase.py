from settings import host, port, database, user, password
from dbmanager import DBManager


def init():
    # Параметры подключения к базе данных PostgreSQL


    # Создание экземпляра класса DBManager
    db_manager = DBManager(host=host, port=port, database=database, user=user, password=password)

    # Создание таблицы vacancies, если она не существует
    create_table_query = """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            );
        """
    cur = db_manager.conn.cursor()
    cur.execute(create_table_query)
    db_manager.conn.commit()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            salary_min INTEGER,
            salary_max INTEGER,
            url VARCHAR(255),
            company_id INTEGER,
            CONSTRAINT company FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE SET NULL
        );
    """
    cur = db_manager.conn.cursor()
    cur.execute(create_table_query)
    db_manager.conn.commit()

init()