class Vacancy:
    __slots__ = ('name', 'link', 'description', 'salary', 'salary_display')

    def __init__(self, file):
        self.name = file.get('name')
        self.link = file.get('link')
        self.description = file.get('description')
        self.salary = file.get('salary')
        self.salary_display = file.get('salary_display')

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
