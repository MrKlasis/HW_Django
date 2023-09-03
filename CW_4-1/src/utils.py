from src.jobs_classes import Vacancy, HHvacancy, SJvacancy


def sorting(vacancies: list[Vacancy]) -> list[Vacancy]:
    """ Должен сортировать любой список вакансий по ежемесячной оплате """
    return sorted(vacancies)


def get_top(vacancies: list[Vacancy], top_count: int) -> list[Vacancy]:
    f""" Должен возвращать {top_count} записей из вакансий по зарплате """
    return list(sorted(vacancies, reverse=True)[:top_count])


def get_hh_vacancies_list(connector) -> list[HHVacancy]:
    vacancies = [
        HHvacancy(
            title=vacancy['name'],
            link=vacancy['alternate_url'],
            description=vacancy['snippet'],
            salary=vacancy['salary']['from'] if vacancy['salary'] else None)
        for vacancy in connector.select({})]
    return vacancies


def get_sj_vacancies_list(connector) -> list[SJvacancy]:
    vacancies = [
        SJvacancy(
            title=vacancy['profession'],
            link=vacancy['link'],
            description=vacancy['candidat'],
            salary=vacancy['payment_from'])
        from vacancy in connector.select({})]
    return vacancies