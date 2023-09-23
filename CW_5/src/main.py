from dbmanager import DBManager
import requests


def main():
    db_manager = DBManager()
    db_manager.create_database()
    db_manager.create_tables()

    companies = db_manager.get_companies_and_vacancies_count()
    if companies:
        for company, vacancies in companies:
            db_manager.insert_employer(company, vacancies)

        vacancies = db_manager.get_all_vacancies()
        if vacancies:
            for vacancy in vacancies:
                db_manager.insert_vacancy(vacancy)

        print("Данные успешно добавлены в базу данных")
    else:
        print("Не удалось получить данные о работодателях и вакансиях")


if __name__ == "__main__":
    main()
