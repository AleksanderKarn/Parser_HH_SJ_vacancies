### файл с функциями программы

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





