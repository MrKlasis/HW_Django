import json
import os


class PathNotFoundError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешней деградации
    """

    def __init__(self, file_path):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Так же проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            if not os.path.exists(self.__data_file):
                with open(self.__data_file, 'w') as file:
                    file.write(json.dumps([]))
        except FileNotFoundError:
            raise PathNotFoundError

    def load_data(self):
        try:
            with open(self.__data_file, 'r') as file:
                file_data = json.load(file)
        except json.JSONDecodeError as e:
            raise MyJsonError(str(e))
        else:
            return file_data

    def insert(self, data: list[dict]):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        file_data = self.load_data()
        with open(self.__data_file, 'w') as file:
            json.dump(file_data + data, file, indent=4, ensure_ascii=False)

    def select(self, query: [dict]):
        """
        Выбор данных из файлов с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        file_data = self.load_data()

        if not query:
            return file_data

        result = []
        for entry in file_data:
            match = True
            for key, value in query.items():
                if key not in entry or entry[key] != value:
                    match = False
                    break
            if match:
                result.append(entry)
        return result

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запросу,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return
        file_data = self.load_data()
        result = []
        for entry in file_data:
            match = True
            for key, value in query.items():
                if key not in entry or entry[key] != value:
                    match = False
                    break
            if not match:
                result.append(entry)
        with open(self.__data_file, 'w') as file:
            json.dump(result, file)


if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select({'id': 'tet'})
    assert data_from_file == [data_for_file]

    df.delete({'id': 1})
    data_from_file = df.select({})

    assert data_from_file == []