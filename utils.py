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


def load_vacancy(jobClass, fn, jobVacancy, text):
    connector = jobClass.get_connector(fn)
    data = jobClass().get_request(text)
    connector.data_file = data
    list_filter = []
    for i in connector.select():
        list_filter.append(jobVacancy(i))

    return list_filter

def load_vacancy_by_job(job, text):
    if (job == '0'):
        return load_vacancy(HH, 'hh.json', HHVacancy, text)
    elif (job == '1'):
        return load_vacancy(SuperJob, 'sj.json', SJVacancy, text)

