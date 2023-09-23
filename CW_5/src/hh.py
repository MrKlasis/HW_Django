import requests


def get_company_info(company_id: int) -> dict:
    '''
    Функция для получания информации о компании
    :param company_id:
    :return:
    '''
    headers = {'User-Agent': 'HH-User-Agent'}
    url = f'https://api.hh.ru/employers/{company_id}'
    response = requests.get(url, headers=headers)
    response = response.json()
    data = {
        'hh_id': response.get('id'),
        'name': response.get('name'),
        'description': response.get('description'),
        'url_company': response.get('alternate_url'),
        'area': response.get('area')['name']
    }
    return data


def get_vacancies_company(company_id: int) -> list[dict]:
    '''
    Функция для получения вакансий работодателя с id=company_id
    :param company_id:
    :return:
    '''
    vacancies = []
    headers = {'User-Agent': 'HH-User-Agent'}
    url = f'https://api.hh.ru/employers/{company_id}'
    response = requests.get(url, headers=headers)
    response = response.json()
    for vacancy in response.get('items'):
        vacancies.append(
            {
                'hh_id': vacancy.get('id'),
                'name': vacancy.get('name'),
                'salary_from': vacancy.get('salary')['from'] if vacancy.get('salary') else None,
                'salary_to': vacancy.get('salary')['to'] if vacancy.get('salary') else None,
                'salary_currency': vacancy.get('salary')['currensy'] if vacancy.get('salary') else None,
                'requirements': vacancy.get('snippet')['requirements'],
                'url': vacancy.get('alternative_url')
            }
        )
    return vacancies
