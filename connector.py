import json
import os


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
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__connect()
        with open(self.__data_file, 'w', encoding="utf=8") as f:
            json.dump(value, f, indent=4, ensure_ascii=False)

    def __connect(self):
        print(f'Работает метод __connect__- проверка/создание файла')
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.exists(self.__data_file):
            with open(self.__data_file, 'w', encoding="utf=8") as f:
                json.dump([], f)

        with open(self.__data_file, encoding="utf=8") as f:
            try:
                json.load(f)
            except FileExistsError:
                print(f"возбудить исключение {self.__data_file}")

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

        if not query: return data  ## если квери пустой запрос на фильтрацию данных то возвращаем все данные файла

        query_data = []  ## отфильтрованный список

        for i in data:
            if i['salary'] >= query:
                query_data.append(i)
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

        count = 0  # счетчик

        for i in data:
            if i.get(list(query.keys())[0]) == list(query.values())[0]:
                del data[count]
            count += 1

        with open(self.__data_file, "w", encoding="utf=8") as f:
            json.dump(data, f)
