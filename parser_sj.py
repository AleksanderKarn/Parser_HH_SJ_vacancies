import requests
from bs4 import BeautifulSoup as BS
import fake_useragent as FU
import json
from abc import ABC, abstractmethod

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
        pass

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__connect()

    def __connect(self):

        print(f'Работает метод __connect__- проверка/создание файла')
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            fp = open(self.__data_file, encoding="utf=8")
        except FileNotFoundError:
            print(f"Создание {self.__data_file}")
            fp = open(self.__data_file, 'w', encoding="utf=8")
            data = []
            json.dump(data, fp)

        else:
            data = json.load(fp)
        finally:
            fp.close()


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
        print(query_data)
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


url = 'https://www.superjob.ru'
ua = FU.UserAgent()



class Engine(ABC):
    file_name: str

    @abstractmethod
    def get_request(self): # должен быть переопределен в дочернем классе
        raise NotImplementedError('Метод get_request должен быть переопределен в дочернем классе!')

    @abstractmethod
    def page_count(self):
        """
        Функция находит колличество страниц
         с вакансиями по  запросу пользователя.
        """
        raise NotImplementedError('Метод page_count должен быть переопределен в дочернем классе!')
     #  soup = get_soup(n=0)

     #  pager_count = int(
     #      soup.find(
     #          'div', attrs={
     #              'class': '_2zPWM _9mI07 _2refD _35SiA _3Gpjg _3vngu _1GAZu'}).find_all('span', recursive=True)[-6].text
     #  )  ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий
     #  return pager_count

    @abstractmethod
    def get_soup(self):
        """
        Функция возвращает данные HTML страницы
        распаршенные при помощи библиотеки BS4
        """
        raise NotImplementedError('Метод get_soup должен быть переопределен в дочернем классе!')
       # if link == None:
       #     if n >= 2:  # условие для обработки любой страницы кроме первой
       #         data = requests.get(
       #             url=f'{url}/vacancy/search/?keywords={text}&page={n}',
       #             headers={"user-agent": ua.random}
       #         )
       #     else:  ## Условие для обработки самой первой страницы у которой нет атрибута page
       #         data = requests.get(
       #             url=f'{url}/vacancy/search/?keywords={text}',
       #             headers={"user-agent": ua.random}
       #         )
       # else:  # если аргумент функции link определен то он используется
       #     data = requests.get(
       #         url=link,
       #         headers={"user-agent": ua.random}
       #     )
       # soup = BS(data.content, 'lxml')
       # return soup


    def get_link(self, soup, list_vacancies):
        """
        Функция проходит циклом по всем ссылкам
        с странциы, вычисляект нужные и добавляет их в список
        """
        raise NotImplementedError('Метод get_link должен быть переопределен в дочернем классе!')
    #    for a in soup.find_all('a'):  ## Цикл по всем ссылкам страницы
    #        if a['href'].split('.')[-1] == 'html':  # выбираю ссылки по ключу 'href' заканчивающиеся на 'html'
    #            if 'vakansii' in a['href'].split(
    #                    '/'):  ## дальше работаю со строкой разбивая ее по слешу и выбирая лиш те строки в которых есть слово vacancy
    #                list_vacancies.append(f"{url}{a['href']}")  # формирую строку - ссылку и складываю ее в список

    @staticmethod
    def get_vacancy(self):
        """
        Функция собирает все вакансии со
        всех страниц в список
        """
        list_vacancies = []  # список вакаансий со страницы сервиса

        for i in range(
                self.page_count() + 1):  # основной цикл програмы проходящий по каждой странице в зависимости от их колличества
            if i == 0:
                continue
            else:  ## условие попадания на первую страницу вакансий
                soup = self.get_soup(n=i)  # получаем все данные с первой страницы
            self.get_link(soup, list_vacancies)
        return list_vacancies


    def get_data(self, link):
        """
        Функция создает объекты вакансий в
        виде словарей в которых ключи названия
        полей а значения - ссылкка, зарплата,
        обязанности и название вакансии
        """
        raise NotImplementedError('Метод get_data должен быть переопределен в дочернем классе!')
   #     soup = self.get_soup(n=0, link=link)  ## генерирую данные из ссылок на вакансии  и достаю нужные
   #     try:
   #         name = soup.find(attrs={'class': "_2s70W _31udi _7mW5l _17ECX _1B2ot _3EXZS _3pAka ofdOE"}).text
   #     except:
   #         name = 'Название не указано'
   #     try:
   #         salary = soup.find(attrs={'class': "f-test-text-company-item-salary"}).text.replace(' ', '')
   #     except:
   #         salary = 'Зп не указана'
   #     try:
   #         description = soup.find(attrs={'class': "_1G5lt _3EXZS _3pAka _3GChV _2GgYH"}).text
   #     except:
   #         description = '-'
   #     vacancy = {
   #         "link": link,
   #         "name": name,
   #         "salary": salary,
   #         "description": description
#
   #     }  ## формирую данные в формате словаря
   #     return vacancy
#

    #file_name = "SJ_vacancyes.json"

    @staticmethod
    def dump_vacancy_json(self, file_name):
        """
        Функция записывает найденные вакансии в Json файл
        """
        list_vac = []  ## список сформированных данных по вакансиям
        for i in self.get_vacancy(self):
            vac = self.get_data(i)
            list_vac.append(vac)
        with open(file_name, "w", encoding="utf=8") as f:  # запись в файл Json данных созданного списка данных по вакансиям
            json.dump(list_vac, f, indent=4, ensure_ascii=False)


    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)







class SuperJob(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям c HH.ru"""
    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name
    def get_request(self):
        self.dump_vacancy_json(self, 'file_name')

    def page_count(self):
        """
        Функция находит колличество страниц
         с вакансиями по  запросу пользователя.
        """
        soup = self.get_soup(n=0)
        pager_count = int(
            soup.find(
                'div', attrs={
                    'class': '_2zPWM _9mI07 _2refD _35SiA _3Gpjg _3vngu _1GAZu'}).find_all('span', recursive=True)[-6].text
        )  ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий
        return pager_count

    def get_soup(self, text=input('Введите название вакансии: '), n=0, link=None):
        """
        Функция возвращает данные HTML страницы
        распаршенные при помощи библиотеки BS4
        """
        if link == None:
            if n >= 2:  # условие для обработки любой страницы кроме первой
                data = requests.get(
                    url=f'{url}/vacancy/search/?keywords={text}&page={n}',
                    headers={"user-agent": ua.random}
                )
            else:  ## Условие для обработки самой первой страницы у которой нет атрибута page
                data = requests.get(
                    url=f'{url}/vacancy/search/?keywords={text}',
                    headers={"user-agent": ua.random}
                )
        else:  # если аргумент функции link определен то он используется
            data = requests.get(
                url=link,
                headers={"user-agent": ua.random}
            )
        soup = BS(data.content, 'lxml')
        return soup


    def get_link(self, soup, list_vacancies):
        """
        Функция проходит циклом по всем ссылкам
        с странциы, вычисляект нужные и добавляет их в список
        """
        for a in soup.find_all('a'):  ## Цикл по всем ссылкам страницы
            if a['href'].split('.')[-1] == 'html':  # выбираю ссылки по ключу 'href' заканчивающиеся на 'html'
                if 'vakansii' in a['href'].split(
                        '/'):  ## дальше работаю со строкой разбивая ее по слешу и выбирая лиш те строки в которых есть слово vacancy
                    list_vacancies.append(f"{url}{a['href']}")  # формирую строку - ссылку и складываю ее в список

    def get_data(self, link):
        """
        Функция создает объекты вакансий в
        виде словарей в которых ключи названия
        полей а значения - ссылкка, зарплата,
        обязанности и название вакансии
        """
        soup = self.get_soup(n=0, link=link)  ## генерирую данные из ссылок на вакансии  и достаю нужные
        try:
            name = soup.find(attrs={'class': "_2s70W _31udi _7mW5l _17ECX _1B2ot _3EXZS _3pAka ofdOE"}).text
            print(name)
        except:
            name = 'Название не указано'
        try:
            salary = soup.find(attrs={'class': "f-test-text-company-item-salary"}).text.replace(' ', '')
            print(salary)
        except:
            salary = 'Зп не указана'
        try:
            description = soup.find(attrs={'class': "_1G5lt _3EXZS _3pAka _3GChV _2GgYH"}).text
            print(description)
        except:
            description = '-'
        vacancy = {
            "link": link,
            "name": name,
            "salary": salary,
            "description": description

        }  ## формирую данные в формате словаря
        return vacancy




class HH(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям с Sj"""
    def get_request(self):
        pass


vac = SuperJob('https://www.superjob.ru', 'SJ_vacancyes.json')

asd = vac.get_connector('SJ_vacancyes.json')