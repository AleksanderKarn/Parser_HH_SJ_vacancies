import requests
from bs4 import BeautifulSoup as BS
import fake_useragent as FU
import json

url = 'https://www.superjob.ru'
ua = FU.UserAgent()

def page_count():
    """
    Функция находит колличество страниц
     с вакансиями по  запросу пользователя.
    """
    soup = get_soup(n=0)

    pager_count = int(
        soup.find(
            'div', attrs={
                'class': '_2zPWM _9mI07 _2refD _35SiA _3Gpjg _3vngu _1GAZu'}).find_all('span',recursive=True)[-6].text
    ) ## методом проб и ошибок вычислил такой вот способ вычленения значения всех страниц вакансий
    return pager_count

def get_soup(text=input('Введите название вакансии: '), n=0, link=None):
    """
    Функция возвращает данные HTML страницы
    распаршенные при помощи библиотеки BS4
    """

    if link == None:

        if n >= 2:
            data = requests.get(
                url=f'{url}/vacancy/search/?keywords={text}&page={n}',
                headers={"user-agent": ua.random}
            )
        else:
            data = requests.get(
                url=f'{url}/vacancy/search/?keywords={text}',
                headers={"user-agent": ua.random}
            )
    else:
        data = requests.get(
            url=link,
            headers={"user-agent": ua.random}
        )
    soup = BS(data.content, 'lxml')
    return soup

def get_link(soup, list_vacancies):
    """
    Функция проходит циклом по всем ссылкам
    с странциы, вычисляект нужные и добавляет их в список
    """
    for a in soup.find_all('a'):  ## Цикл по всем ссылкам страницы
        if a['href'].split('.')[-1] == 'html':  # выбираю ссылки по ключу 'href' заканчивающиеся на 'html'
            if 'vakansii' in a['href'].split(
                    '/'):  ## дальше работаю со строкой разбивая ее по слешу и выбирая лиш те строки в которых есть слово vacancy
                list_vacancies.append(f"{url}{a['href']}")  # формирую строку - ссылку и складываю ее в список


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
        get_link(soup, list_vacancies)
    return list_vacancies


def get_data(link):
    """
    Функция создает объекты вакансий в
    виде словарей в которых ключи названия
    полей а значения - ссылкка, зарплата,
    обязанности и название вакансии
    """
    soup = get_soup(n=0, link=link) ## генерирую данные из ссылок на вакансии  и достаю нужные
    try:
        name = soup.find(attrs={'class': "_2s70W _31udi _7mW5l _17ECX _1B2ot _3EXZS _3pAka ofdOE"}).text
    except:
        name = 'Название не указано'
    try:
        salary = soup.find(attrs={'class': "f-test-text-company-item-salary"}).text.replace(' ', '')
    except:
        salary = 'Зп не указана'
    try:
        description = soup.find(attrs={'class': "_1G5lt _3EXZS _3pAka _3GChV _2GgYH"}).text
    except:
        description = '-'
    vacancy = {
        "name": name,
        "salary": salary,
        "description": description,
        "link": link
    }  ## формирую данные в формате словаря
    return vacancy


def dump_vacancy_json():
    """
    Функция записывает найденные вакансии в Json файл
    """
    list_vac = [] ## список сформированных данных по вакансиям
    for i in get_vacancy():
        vac = get_data(i)
        list_vac.append(vac)

    with open("SJ_vacancyes.json", "w", encoding="utf=8") as f: #
        json.dump(list_vac, f, indent=4, ensure_ascii=False)

dump_vacancy_json()