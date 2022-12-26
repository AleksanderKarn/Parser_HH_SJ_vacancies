### основное тело программы
import json
from utils import sorting, get_top, load_vacancy_by_job
from jobs_classes import HHVacancy, SJVacancy
commandList = {
        'list': "Вывести все вакансии sorted",
        'top 10': "Вывести топ 10 ваканчий по ЗП",
        'help': "Вывести список доступных команд",
        'exit': "Выход из программы",
        'len': "Вывести колличество вакансий всего"
    }

if __name__ == '__main__':
    job = input('Выберите сервис HH(0) или SJ(1): ')
    if not job or (job != '1' and job != '0'):
        print('Error')

    text = input('Введите название вакансии, по умолчанию используется "Python": ')

    if not text:
        text = 'Python'

    listVacancy = load_vacancy_by_job(job, text)

    while True: ## цикл для работы с данными файла при помощи доступных команд
        print('*' * 60)
        command = input('Введите команду: ')
        print('*' * 60)

        if command == 'exit':
            print('Завершение работы программы...')
            break
        elif command == 'list':
            with open('sj.json', encoding="utf-8") as f:
                data = json.load(f)
                sort_list = sorting(listVacancy)
            for i in sort_list:
                print(i)
        elif command == 'help':
            print(commandList)
        elif command == 'len':
            if job == 0:
                a = HHVacancy
                print(a.get_count_of_vacancy('hh.json'))
            else:
                a = SJVacancy
                print(a.get_count_of_vacancy('sj.json'))
        else:
            com = command.split(' ')[1]
            if len(command.split(' ')) > 1 and command.split(' ')[0] == 'top':
                top_vacancy = get_top(listVacancy, int(com))
                for i in top_vacancy:
                    print(i)
            else:
                print('Не верная команда! Введите help для просмотра доступных команд')
