

def read_data(filename):
    """
    Читаем данные из файлов: темы и слова
    :param filename: путь к файлу
    :return:
    """
    with open(filename, "r", encoding="utf-8") as file_data:
        datalist = []
        for line in file_data:
            line_list = line.split(",")
            if len(line_list) == 2:
                datalist.append(line_list)
        return datalist


def read_file(filename):
    """
    Читает содержимое файла
    :param filename: путь к файлу
    :return:
    """
    with open(filename, "r", encoding="utf-8") as file_data:
        return file_data.read()
