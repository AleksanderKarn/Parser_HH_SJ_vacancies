import requests
from bs4 import BeautifulSoup as BS
import fake_useragent as FU
import json
from abc import ABC, abstractmethod
from connector import Connector


ua = FU.UserAgent()

url_dict = {
            'url_hh': 'https://hh.ru',
            'url_sj': 'https://www.superjob.ru'
}

class Engine(ABC):
    file_name: str

    #def __init__(self, url, file_name, text):
    #    self.url = url
    #    self.file_name = file_name
    #    self.text = text

    @abstractmethod
    def get_request(self, text):  # должен быть переопределен в дочернем классе
        raise NotImplementedError('Метод __get_request__ должен быть переопределен в дочернем классе!')

    @abstractmethod
    def page_count(self):
        """
        Функция находит колличество страниц
         с вакансиями по  запросу пользователя.
        """
        raise NotImplementedError('Метод __page_count__ должен быть переопределен в дочернем классе!')

    @abstractmethod
    def get_soup(self, text):
        """
        Функция возвращает данные HTML страницы
        распаршенные при помощи библиотеки BS4
        """
        raise NotImplementedError('Метод __get_soup__ должен быть переопределен в дочернем классе!')

    def get_link(self, soup, list_vacancies):
        """
        Функция проходит циклом по всем ссылкам
        с странциы, вычисляект нужные и добавляет их в список
        """
        raise NotImplementedError('Метод __get_link__ должен быть переопределен в дочернем классе!')

    @abstractmethod
    def get_data(self, link):
        """
        Функция создает объекты вакансий в
        виде словарей в которых ключи названия
        полей а значения - ссылкка, зарплата,
        обязанности и название вакансии
        """
        raise NotImplementedError('Метод __get_data__ должен быть переопределен в дочернем классе!')

    @staticmethod
    def get_vacancy(self, text):
        """
        Функция собирает все вакансии со
        всех страниц в список
        """
        list_vacancies = []  # список вакаансий со страницы сервиса
        for i in range(
                self.page_count(text) + 1):  # основной цикл програмы проходящий по каждой странице в зависимости от их колличества
            if i == 0:
                continue
            else:  ## условие попадания на первую страницу вакансий
                soup = self.get_soup(text, n=i)  # получаем все данные с первой страницы
            self.get_link(soup, list_vacancies)
        return list_vacancies

    @staticmethod
    def dump_vacancy_json(self, text):
        """
        Функция записывает найденные вакансии в Json файл
        """
        list_vac = []  ## список сформированных данных по вакансиям
        for i in self.get_vacancy(self, text):
            vac = self.get_data(i)
            list_vac.append(vac)
        return list_vac
        #with open(file_name, "w",
        #          encoding="utf=8") as f:  # запись в файл Json данных созданного списка данных по вакансиям
        #    json.dump(list_vac, f, indent=4, ensure_ascii=False)

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям с Sj"""

    def get_request(self, text):
       # self.dump_vacancy_json(self, text)
        return self.dump_vacancy_json(self, text)


    def page_count(self, text):
        soup = self.get_soup(text, n=0)

        pager_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text
        )  ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий
        print(f"Всего страниц: {pager_count}")
        return 1

    def get_soup(self, text, n=0, link=None):
        if link == None:
            if n >= 2:  # условие для обработки любой страницы кроме первой
                print(f'идем на {n} страницу')
                data = requests.get(
                    url=f'{url_dict["url_hh"]}/search/vacancy?text={text}&from=suggest_post&area=1&page={n}',
                    headers={"user-agent": ua.random}
                )
            else:  ## Условие для обработки самой первой страницы у которой нет атрибута page
                print('Идем на первую страницу')
                data = requests.get(
                    url=f'{url_dict["url_hh"]}/search/vacancy?text={text}',
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
        for a in soup.find_all('a', attrs={'class': 'serp-item__title'}):  ## Цикл по всем ссылкам страницы
            list_vacancies.append(f"{a.attrs['href'].split('?')[0]}")

    def get_data(self, link):
        soup = self.get_soup(n=0, link=link, text=None)  ## генерирую данные из ссылок на вакансии  и достаю нужные
        try:
            name = soup.find(attrs={'class': "bloko-header-section-1"}).text
        except:
            name = 'Название не указано'
        try:
            salary = soup.find(attrs={'class': "bloko-header-section-2 bloko-header-section-2_lite"}).text.replace(
                '\xa0',
                '')
            print(salary)
        except:
            salary = 'Зп не указана'
        try:
            description = soup.find(attrs={'class': "g-user-content"}).text
        except:
            description = '-'
        vacancy = {
            "link": link,
            "name": name,
            "salary": salary,
            "description": description

        }  ## формирую данные в формате словаря
        return vacancy


class SuperJob(Engine):
    """создает файл джейсон с данными по нужным нам вакансиям c HH.ru"""

    def get_request(self, text):
        return self.dump_vacancy_json(self, text)

    def page_count(self, text):
        soup = self.get_soup(text, n=0)
        pager_count = int(
            soup.find(
                'div', attrs={
                    'class': '_2zPWM _9mI07 _2refD _35SiA _3Gpjg _3vngu _1GAZu'}).find_all('span', recursive=True)[
                -6].text
        )  ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий
        return pager_count

    def get_soup(self, text, n=0, link=None):
        if link == None:
            if n >= 2:  # условие для обработки любой страницы кроме первой
                data = requests.get(
                    url=f'{url_dict["url_sj"]}/vacancy/search/?keywords={text}&page={n}',
                    headers={"user-agent": ua.random}
                )
            else:  ## Условие для обработки самой первой страницы у которой нет атрибута page
                data = requests.get(
                    url=f'{url_dict["url_sj"]}/vacancy/search/?keywords={text}',
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
        for a in soup.find_all('a'):  ## Цикл по всем ссылкам страницы
            if a['href'].split('.')[-1] == 'html':  # выбираю ссылки по ключу 'href' заканчивающиеся на 'html'
                if 'vakansii' in a['href'].split(
                        '/'):  ## дальше работаю со строкой разбивая ее по слешу и выбирая лиш те строки в которых есть слово vacancy
                    list_vacancies.append(f"{url_dict['url_sj']}{a['href']}")  # формирую строку - ссылку и складываю ее в список

    def get_data(self, link):
        soup = self.get_soup(n=0, link=link, text=None)  ## генерирую данные из ссылок на вакансии  и достаю нужные
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
