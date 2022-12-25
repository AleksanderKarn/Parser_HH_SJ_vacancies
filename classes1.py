### файл с классами
from abc import ABC, abstractmethod
import json
import os.path


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, df):
        print(f'инициализация экземпляра класса Connector')
        self.__data_file = df
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__connect()
        with open(self.__data_file, 'w', encoding="utf=8") as f:
            json.dump(f, value)

    def __connect(self):

        print(f'Работает метод __connect__- проверка/создание файла')
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """ 
        if not os.path.exists(self.__data_file):
            with open(self.__data_file, 'w', encoding="utf=8") as f:
                json.dump([], f)
            
            return

        # print('проверить на деградацию и возбудить исключение')
        with open(self.__data_file, encoding="utf=8") as f:
            try:
                json.load(f)
            except FileExistsError:
                print(f"возбудить исключение {self.__data_file}")


        # try:
        #     fp = open(self.__data_file, encoding="utf=8")
        # except FileNotFoundError:
        #     print(f"Создание {self.__data_file}")
        #     fp = open(self.__data_file, 'w', encoding="utf=8")
        #     data = []
        #     json.dump(data, fp)

        # else:
        #     data = json.load(fp)
        # finally:
        #     fp.close()


    def insert(self, data):
        print(f'Работает метод __Insert__ идет запись данных...')
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, encoding="utf=8") as f:
            r_data = json.load(f)
            r_data.append(data)
        with open(self.__data_file, "w", encoding="utf=8") as f:
            json.dump(r_data, f)


    def select(self, query):
        print(f'работает метод __select__ фильтруект по {query}')
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, encoding="utf-8") as f:
            data = json.load(f)

        if not len(query): return data  ## если квери пустой запрос на фильтрацию данных то возвращаем все данные файла

        query_data = []  ## отфильтрованный список

        for i in data:
            if i[f'{list(query.keys())[0]}'] == f'{list(query.values())[0]}':
                query_data.append(i)
        return query_data

    def delete(self, query):
        print(f'Работает метод __delete__ - удаляет {query}')
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query): return None

        with open(self.__data_file, encoding="utf=8") as f:
            data = json.load(f)

        count = 0 # счетчик

        for i in data:

            print(i.get(list(query.keys())[0]))
            print('*' * 40)
            print(list(query.values())[0])

            if i.get(list(query.keys())[0]) == list(query.values())[0]:
                del data[count]
            count += 1

        with open(self.__data_file, "w", encoding="utf=8") as f:
            json.dump(data, f)




class Engine(ABC):
    @abstractmethod
    def get_request(self): # должен быть переопределен в дочернем классе
        pass


    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


#requestData = [
#    {
#        name_vacancy: 'name_vacancy',
#        link: 'link',
#        duties: 'duties',
#        salary: 100000
#    }
#]


class HH(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям c HH.ru"""
    def get_request(self):
       # return requestData
        pass


class SuperJob(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям с Sj"""
    def get_request(self):
        return requestData




class Vacancy:
    __slots__ = ('name', 'link', 'duties', 'salary')

    def __init__(self, file):
        self.name = file.get('name')
        self.link = file.get('link')
        self.duties = file.get('duties')
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

    @property
    def get_count_of_vacancy(self, vac_lst):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        return len(vac_lst)




class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """





class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """



# def select(query):
#     """
#     Выбор данных из файла с применением фильтрации
#     query содержит словарь, в котором ключ это поле для
#     фильтрации, а значение это искомое значение, например:
#     {'price': 1000}, должно отфильтровать данные по полю price
#     и вернуть все строки, в которых цена 1000
#     """
#     with open("vacancy_list.json", encoding="utf-8") as f:
#         data = json.load(f)

#     if not len(query): return data  ## если квери пустой запрос на фильтрацию данных то возвращаем все данные файла

#     query_data = []  ## отфильтрованный список

    # for i in data:
    #     if i[f'{list(query.keys())[0]}'] == f'{list(query.values())[0]}':
    #         query_data.append(i)
    #         print(query_data)
    # return query_data

# query = {"salary": "з/п не указана"}

# #select(query)

# file = 'vacancy_list.json'
# def func(file):
#     """
#     функция создает список фильтрованный вакансий
#     """
#     obj_list = []
#     vacancy_connector = Engine.get_connetor(file)

#     vacancy_list = vacancy_connector.select({"salary": "з/п не указана"})
#     for vacancy in vacancy_list:
#         vac_obj = HHVacancy(vacancy) # создал экземпляр класса

#         obj_list.append(vac_obj) # добавил его в список
#         print(vac_obj)
#     return obj_list  # возвращаю список обьекктов класса hhru

# print(func(file))
# #print(v)

def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies)




def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    return sorted(vacancies)[:top_count]


#def getHHVacancies(fileName):
#    hhRawVacancies = HH.get_request()
#    hhConnector = HH.get_connector(fileName)
#    for vacancy in hhRawVacancies:
#        hhConnector.insert(vacancy)

if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id': 1})
    data_from_file = df.select(dict())
    assert data_from_file == []

    # Получить вакансии с HH
    fileName = 'hh.json'
   # getHHVacancies(fileName)


    hhConnector = HH.get_connector(fileName)
    hhVacancies =[]

    for vacancy in hhConnector.select({}):
        hhVacancies.append(HHVacancy(vacancy))
    
    
    # hhVacancies = []
