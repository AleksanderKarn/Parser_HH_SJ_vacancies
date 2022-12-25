from class_Engine import Engine, HH, SuperJob
import re

class Vacancy:
    __slots__ = ('name', 'link', 'description', 'salary')

    def __init__(self, file):

        self.name = file.get('name')
        self.link = file.get('link')
        self.description = file.get('description')
        self.salary = file.get('salary')


    def __str__(self):
        return f'{self.name}, зарплата: {self.salary} руб/мес'

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def __iter__(self):
        pass

    def __next__(self):
        pass



class CountMixin:


    def get_count_of_vacancy(self, count):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        return len(count)



class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """

    def __str__(self):
        return f'HH: {self.name}. | Зарплата: {self.salary}'



class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """

    def __str__(self):
        return f'SJ: {self.name}. | Зарплата: {self.salary}'
#
#def sorting(vacancies):
#    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
#    d = {}
#
#    for i in vacancies:
#        d[i] = [int(s) for s in re.findall(r'\b\d+\b', i.salary)][0]
#        s_d = sorted(d.values())
#        print(s_d)
#    return s_d


#file = 'SJ_vacancyes.json'
##file = 'HH_vacancyes.json'
#
#text = input('Введите название вакансии: ')
#def func(file, text):
#    """
#    функция создает список фильтрованный вакансий
#    """
#    obj_list = []
#   # text = input('Введите название вакансии: ')
#    vacancy_connector = Engine.get_connector(file)
#
#    vacancy_list = vacancy_connector.select({'salary': '50000'})
#    for vacancy in vacancy_list:
#        vac_obj = SJVacancy(vacancy) # создал экземпляр класса
#        obj_list.append(vac_obj) # добавил его в список
#       # sorting([int(s) for s in re.findall(r'\b\d+\b', i.salary)][0])
#
#    sorting(obj_list)
#    return obj_list  # возвращаю список обьекктов класса hhru
#
#func(file, text)