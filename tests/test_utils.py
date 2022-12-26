from utils import sorting

d = [
    {
        "link": "https://www.superjob.ru/vakansii/programmist-1c-44933587.html",
        "name": "Программист 1С",
        "salary": 150000,
        "salary_display": "от150000₽/месяц",
        "description": "Разработкой нового, модернизацией и корректировкой существующего функционала продуктов на платформе 1С:8.3. Доработкой используемых…Хорошее знание стандартных конфигураций 1С. Уверенные знания и навыки…"
    },

    {
        "link": "https://www.superjob.ru/vakansii/lead-python-developer-44950901.html",
        "name": "Асессор-разработчик (поисковая выдача)",
        "salary": 65000,
        "salary_display": "до65000₽/месяц",
        "description": "Изучать результаты поисковой выдачи по набору запросов. Решать, каким источникам можно или нельзя доверять. Консультироваться…Ответственно выполняете задания, когда никто не контролирует"
    },
    {
        "link": "https://www.superjob.ru/vakansii/glavnyj-specialist-informacionnoj-bezopasnosti-44929138.html",
        "name": "Специалист по кадрам",
        "salary": 90000,
        "salary_display": "от90000₽/месяц",
        "description": "Полное ведение кадрового учета и делопроизводства. Ведение данных по квотированию рабочих мест. Сдача статистической отчетностиВысшее образование. Наличие справки о несудимости"
    },
    {
        "link": "https://www.superjob.ru/vakansii/senior-python-developer-45166813.html",
        "name": "Название ваканчии не указано",
        "salary": 0,
        "salary_display": "Зп не указана",
        "description": "-"
    }
]


c = [
    {
        "link": "https://www.superjob.ru/vakansii/programmist-1c-44933587.html",
        "name": "Программист 1С",
        "salary": 150000,
        "salary_display": "от150000₽/месяц",
        "description": "Разработкой нового, модернизацией и корректировкой существующего функционала продуктов на платформе 1С:8.3. Доработкой используемых…Хорошее знание стандартных конфигураций 1С. Уверенные знания и навыки…"
    },

    {
        "link": "https://www.superjob.ru/vakansii/glavnyj-specialist-informacionnoj-bezopasnosti-44929138.html",
        "name": "Специалист по кадрам",
        "salary": 90000,
        "salary_display": "от90000₽/месяц",
        "description": "Полное ведение кадрового учета и делопроизводства. Ведение данных по квотированию рабочих мест. Сдача статистической отчетностиВысшее образование. Наличие справки о несудимости"
    },

    {
        "link": "https://www.superjob.ru/vakansii/lead-python-developer-44950901.html",
        "name": "Асессор-разработчик (поисковая выдача)",
        "salary": 65000,
        "salary_display": "до65000₽/месяц",
        "description": "Изучать результаты поисковой выдачи по набору запросов. Решать, каким источникам можно или нельзя доверять. Консультироваться…Ответственно выполняете задания, когда никто не контролирует"
    },

    {
        "link": "https://www.superjob.ru/vakansii/senior-python-developer-45166813.html",
        "name": "Название ваканчии не указано",
        "salary": 0,
        "salary_display": "Зп не указана",
        "description": "-"
    }
]
def test_sorting(d):
    assert sorting(d) == c
    assert sorting(d) != []