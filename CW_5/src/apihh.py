from urllib import response
import requests


class ApiHH():

    def get_companies(self, companies_ids):
        companies = []
        for company_id in companies_ids:
            url = f"https://api.hh.ru/companies/{company_id}"
            response = requests.get(url)

            if response.status_code == 200:
                company_data = response.get()
                companies.append(company_data)
            else:
                print(f"Ошибка при получении данных для компании с ID {company_id}")

        return companies

    def get_vacancies_by_company(self, employer_id):
        if response.status_code == 200:
            vacancies_data = response.json()
            vacancies = vacancies_data.get("items", [])
        else:
            print(f"Ошибка при получении данных для компании с ID {employer_id}")

        return vacancies


