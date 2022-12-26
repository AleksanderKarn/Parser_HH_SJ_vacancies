### файл с функциями программы
from class_Engine import HH, SuperJob
from jobs_classes import HHVacancy, SJVacancy

def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies, reverse=True)


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    ## взять N первых строк вакансий
    count = 0
    top_vacancies = []
    for i in sorting(vacancies):
        if count == top_count:
            return top_vacancies
        top_vacancies.append(i)
        count += 1

def load_vacancy(job_class, fn, job_vacancy, text):
    """
    Функция инициализирует коннектор и экземпляр
     класса вакансий, далше проходит цуиклом
     по отфильтрованным  вакансиям и собиравет
     их в список
    :param jobClass: имя Класса вакансий
    :param fn:  имя файла с вакансиями в json
    :param jobVacancy: имя класса вакансии
    :param text: названиек вакансии
    :return: список объктов вакакнсий отфильтрованный по зарплате
    """
    connector = job_class.get_connector(fn)
    data = job_class().get_request(text)
    connector.data_file = data
    list_filter = []
    for i in connector.select():
        list_filter.append(job_vacancy(i))
    return list_filter

def load_vacancy_by_job(job, text):
    """
    Функция определяет входные данные
     для поиска в зависимости от ввода пользователя
    :param job: "числовое значение введенное пользователем при выборе сервиса поиска работы"
    :param text: "наименование профессии по которой осуществляется поиск "
    :return: "входные данные (значения апгументов ) для функции '__load_vacancy__'"
    """
    if (job == '0'):
        return load_vacancy(HH, f"vac_{text}.json", HHVacancy, text)
    elif (job == '1'):
        return load_vacancy(SuperJob, f"vac_{text}.json", SJVacancy, text)

