### основное тело программы
from utils import sorting, get_top, load_vacancy_by_job, print_vacancies
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
    query = int(input('введите фильтр: '))

    list_vacancy = load_vacancy_by_job(job, text, query)

    while True:  ## цикл для работы с данными файла при помощи доступных команд
        print('*' * 60)
        command = input('Введите команду: ')
        print('*' * 60)

        if command == 'exit':
            print('Завершение работы программы...')
            break
        elif command == 'list':
            print_vacancies(sorting(list_vacancy))
        elif command == 'help':
            print(commandList)
        elif command == 'len':
            if job == 0:
                print(HHVacancy.get_count_of_vacancy(list_vacancy))
            else:
                print(SJVacancy.get_count_of_vacancy(list_vacancy))
        else:
            com = command.split(' ')
            if len(com) > 1 and com[0] == 'top' and com[1]:
                print_vacancies(get_top(list_vacancy, int(com[1])))
            else:
                print('Не верная команда! Введите help для просмотра доступных команд')
