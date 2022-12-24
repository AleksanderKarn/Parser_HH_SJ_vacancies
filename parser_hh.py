import requests
from bs4 import BeautifulSoup as BS
import fake_useragent as FU
import json

url = 'https://hh.ru'
ua = FU.UserAgent()

def page_count():
    """
    Функция находит колличество страниц
     с вакансиями по  запросу пользователя.
    """
    soup = get_soup(n=0)

    pager_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text
    ) ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий

    return pager_count


def get_soup(text=input('Введите название вакансии: '), n=0, link=None):
    """
    Функция возвращает данные HTML страницы
    распаршенные при помощи библиотеки BS4
    """
    if link == None:
        if n >= 2: # условие для обработки любой страницы кроме первой
            data = requests.get(
                url=f'{url}/search/vacancy?text={text}&from=suggest_post&area=1&page={n}',
                headers={"user-agent": ua.random}
            )
        else: ## Условие для обработки самой первой страницы у которой нет атрибута page
            data = requests.get(
                url=f'{url}/search/vacancy?text={text}',
                headers={"user-agent": ua.random}
            )

    else: # если аргумент функции link определен то он используется
        data = requests.get(
            url=link,
            headers={"user-agent": ua.random}
        )
    soup = BS(data.content, 'lxml')
    return soup


def get_vacancy():
    """
    Функция собирает все вакансии со
    всех страниц в список
    """
    list_vacancies = [] # список вакаансий со страницы сервиса

    for i in range(page_count()+1): # основной цикл програмы проходящий по каждой странице в зависимости от их колличества
        if i == 0:
            continue
        else: ## условие попадания на первую страницу вакансий
            soup = get_soup(n=i) # получаем все данные с первой страницы
        get_link(soup, list_vacancies) # используем подготовленную функцию для прохода по всем ссылкам
    return list_vacancies


def get_link(soup, list_vacancies):
    """
    Функция проходит циклом по всем ссылкам
    с странциы, вычисляект нужные и добавляет их в список
    """
    for a in soup.find_all('a', attrs={'class': 'serp-item__title'}):  ## Цикл по всем ссылкам страницы
        list_vacancies.append(f"{a.attrs['href'].split('?')[0]}")

def get_data(link):
    """
    Функция создает объекты вакансий в
    виде словарей в которых ключи названия
    полей а значения - ссылкка, зарплата,
    обязанности и название вакансии
    """
    soup = get_soup(n=0, link=link) ## генерирую данные из ссылок на вакансии  и достаю нужные
    try:
        name = soup.find(attrs={'class': "bloko-header-section-1"}).text
    except:
        name = 'Название не указано'
    try:
        salary = soup.find(attrs={'class': "bloko-header-section-2 bloko-header-section-2_lite"}).text.replace('\xa0',
                                                                                                               '')
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

file_name = "HH_vacancyes.json"

def dump_vacancy_json(file_name):
    """
    Функция записывает найденные вакансии в Json файл
    """
    list_vac = [] ## список сформированных данных по вакансиям
    for i in get_vacancy():
        vac = get_data(i)
        list_vac.append(vac)
    with open(file_name, "w", encoding="utf=8") as f: # запись в файл Json данных созданного списка данных по вакансиям
        json.dump(list_vac, f, indent=4, ensure_ascii=False)

dump_vacancy_json(file_name)