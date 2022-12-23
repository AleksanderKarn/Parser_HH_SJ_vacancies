from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup as BS
import fake_useragent as FU
import time
import json



url = 'https://www.superjob.ru'
def get_vacancy(text):

    ua = FU.UserAgent()  # экземпляр класса фейкюзер агента
    data = requests.get(
        url=f'{url}/vacancy/search/?keywords={text}',
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BS(data.content, 'lxml')
    l = []
    for i in range(4):
        print(i)
        if i == 0:
            print('__if__')
            continue
        elif i == 1:
            print('__elif__')

            data = requests.get(
                url=f'{url}/vacancy/search/?keywords={text}',
                headers={"user-agent": ua.random}
            )
        #   if data.status_code != 200:
        #       print(data.status_code)
        #       continue
        #   if not data:
        #       break
            soup = BS(data.content, 'lxml')

            for i in soup.find_all('a'):
                if i['href'].split('.')[-1] == 'html':
                    if 'vakansii' in i['href'].split('/'):
                        l.append(f"{url}{i['href']}")
        else:
            print('__else__')
            data = requests.get(
                url=f'{url}/vacancy/search/?keywords={text}&page={i}',
                headers={"user-agent": ua.random}
            )
            soup = BS(data.content, 'lxml')

            for i in soup.find_all('a'):
                if i['href'].split('.')[-1] == 'html':
                    if 'vakansii' in i['href'].split('/'):
                        l.append(f"{url}{i['href']}")

    return l

def get_data(link):
    ua = FU.UserAgent()  # экземпляр класса фейкюзер агента
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BS(data.content, 'lxml')
    try:
        name = soup.find(attrs={'class': "_2s70W _31udi _7mW5l _17ECX _1B2ot _3EXZS _3pAka ofdOE"}).text
    except:
        name ='Название не указано'
    try:
        salary = soup.find(attrs={'class': "f-test-text-company-item-salary"}).text.replace(' ', '')
        print(salary)
    except:
        salary ='Зп не указана'
    try:
        description = soup.find(attrs={'class': "_1G5lt _3EXZS _3pAka _3GChV _2GgYH"}).text
    except:
        description ='-'
    vacancy = {
        "name": name,
        "salary": salary,
        "description": description,
        "link": link
    }

    return vacancy

text = 'python'


if __name__ == "__main__":
    list_vac = []
    for i in get_vacancy(text):
        vac = get_data(i)
        list_vac.append(vac)
    with open("SJ_vacancyes.json", "w", encoding="utf=8", ) as f:
        json.dump(list_vac, f, indent=4, ensure_ascii=False)



