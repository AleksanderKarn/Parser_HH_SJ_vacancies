### основное тело программы
from class_Engine import HH, SuperJob
from jobs_classes import HHVacancy, SJVacancy
import json
from utils import sorting, get_top

commandList = {
        'list': "Вывести все вакансии sorted",
        'top 10': "Вывести топ 10 ваканчий по ЗП",
        'help': "Вывести список доступных команд",
        'exit': "Выход из программы"
    }


def load_vacancy(jobClass, fn, jobVacancy, text):
    connector = jobClass.get_connector(fn)
    data = jobClass().get_request(text)

    connector.data_file = data
    list_filter = []
    for i in connector.select():
        list_filter.append(jobVacancy(i))

    return list_filter


def load_vacancy_by_job(job, text):
    if (job == '0'):
        return load_vacancy(HH, 'hh.json', HHVacancy, text)
    elif (job == '1'):
        return load_vacancy(SuperJob, 'sj.json', SJVacancy, text)


if __name__ == '__main__':
    job = input('Выберите сервис HH(0) или SJ(1): ')
    if not job or (job != '1' and job != '0'):
        print('Error')


    text = input('Введите название вакансии, по умолчанию используется "Python": ')

    if not text:
        text = 'Python'

    listVacancy = load_vacancy_by_job(job, text)


    while True:
        command = input('Введите команду: ')

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
        else:
            com = command.split(' ')[1]
            if len(command.split(' ')) > 1 and command.split(' ')[0] == 'top':
                top_vacancy = get_top(listVacancy, int(com))
                for i in top_vacancy:
                    print(i)
            else:
                print('Не верная команда! Введите help для просмотра доступных команд')
