### основное тело программы
from class_Engine import HH, SuperJob
from jobs_classes import HHVacancy, SJVacancy


def load_vacancy(jobClass, fn, jobVacancy, text):
    connector = jobClass.get_connector(fn)
  # data = jobClass().get_request(text)

#    connector.data_file = data
    l = []
    for i in connector.select():
        l.append(jobVacancy(i))
    return l



def load_vacancy_by_job(job, text):

    if (job == '0'):
        return load_vacancy(HH, 'hh.json', HHVacancy, text)
    elif (job == '1'):
        return load_vacancy(SuperJob, 'sj.json', SJVacancy, text)


if __name__ == '__main__':
    job = input('Выберите сервис HH(0) или SJ(1): ')
    if not job or (job != '1' and job != '0'):
        print('Error')

    text = input('Введите название вакансии: ')

   # select = input('?Введите минимальную зарплату: ')

    if not text:
        text = 'Python'
    print(text)
    listVacancy = load_vacancy_by_job(job, text)

    commandList = [
        'list',  # вывести все вакансии sorted
        'top',  # вывести топ top 1000
        'help',  #
        'exit'  # выход
    ]
    while True:
        command = input('Введите команду: ')

        if command == 'exit':
            break
        elif command == 'list':
            print('list')
        elif command == 'help':
            print(commandList)
        else:
            c = command.split(' ')
            if c[0] == 'top' and c[1]:
                print('top')
            else:
                print('Error')