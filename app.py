""" Данный модуль предназначен для поиска информации с сайта по адресам из csv-файла  """
from selenium import webdriver
from typing import Dict, Tuple, List, Union
import sqlite3
from collections import defaultdict
import json
import csv
from pages.quotes_page import QuotesPage


""" Данный модуль предназначен для поиска информации с сайта по адресам из csv-файла  """


chrome = webdriver.Chrome(
    executable_path="/Users/BARAK/Desktop/sovcom/chromedriver.exe")
chrome.get("https://egrp365.ru/")


def address_reader(filename) -> List[str]:
    """
    Функция для создания списка запросов из csv-файла
    """
    columns = defaultdict(list)
    with open(filename, encoding='utf8') as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        # read a row as {column1: value1, column2: value2,...}
        for row in reader:
            for (k, v) in row.items():  # go over each column name and value
                # append the value into the appropriate list
                columns[k].append(v)
                # based on column name k)
    return columns['Adress']


def get_data(address):
    """
    Функция для обработки полученных после скрейпинга с сайта результатов.

    """
    page = QuotesPage(chrome)  # создает экземпляр класса QuotesPage
    # получаем данные с помощью функции search_for_info
    scrapped_data = page.search_for_info(address)
    cadast_num = None
    found_address = None
    cadast_link = None
    full_json = None
    full_json = ''
    # если возращенные данные типа str то переводим в нужный для дальнейшей обработки формат типа {"Кадастровый номер" : "11:12:1702003:968"}
    if isinstance(scrapped_data, str):
        list_data = scrapped_data.split('\n')
        dict_type = ['{"'+e.replace(' — ', '" : "')+'"}'
                     for e in list_data if e is not '']
        scrapped_data = dict_type  # передаем обратно

    if scrapped_data:
        for data in scrapped_data:
            new_data = str(data).replace('\'', '\"').replace(
                'None', '"None"')  # to convert to json нужно удостовериться что нет одинарных кавычек
            # создает словарь для хранения строк с результатами поиска
            res = json.loads(new_data)

            if 'Почтовый адрес' in str(data):
                found_address = res['Почтовый адрес']
            if "Другое написание адреса" in str(data):
                found_address = res['Другое написание адреса']
            if 'Кадастровый номер дома' in str(data):
                draft_num = res['link']
                index = draft_num.find('=')+1
                end_index = len(draft_num)
                cadast_num = draft_num[index:end_index]
            if 'Кадастровый номер' in str(data):
                cadast_num = res['Кадастровый номер']
            if 'Кадастровая карта' in str(data):
                cadast_link = res['link']
                print(cadast_link)

            full_json = full_json + new_data  # to store full json request
    return cadast_num, found_address, cadast_link, full_json


def create_search_table():
    """
    Функция для создания таблицы для хранения результатов поиска
    столбцы: idP integer primary key AUTOINCREMENT NOT NULL, cadast_num text, found_address text, cadast_link text, full_json text
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS property(idP integer primary key AUTOINCREMENT NOT NULL, cadast_num text, found_address text, cadast_link text, full_json text, request_address text NOT NULL, FOREIGN KEY(request_address) REFERENCES requests(req_name) ON DELETE CASCADE)')
    connection.commit()
    connection.close()


def create_requests_table():
    """
    Функция для создания таблицы для хранения поиска
    столбцы: RequestsId integer primary key AUTOINCREMENT NOT NULL, req_name text NOT NULL
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS requests(RequestsId integer primary key AUTOINCREMENT NOT NULL, req_name text NOT NULL)')
    connection.commit()
    connection.close()


def add_search_result(cadast_num, found_address, cadast_link, full_json, address):
    """
    Функция для записи передаваемых значений в таблицу property
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO property VALUES(NULL,?,?,?,?,?)',
                   (cadast_num, found_address, cadast_link, full_json, address))
    connection.commit()
    connection.close()


def add_requests(address):
    """
    Функция для записи передаваемых значений в таблицу requests
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO requests VALUES(NULL, ?)', (address,))
    connection.commit()
    connection.close()


# После получения результатов написать скрипты для следующего анализа:

def requests_notfound():
    """
    Функция для определения количества найденных и не найденных объектов
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT SUM(CASE WHEN found_address IS NULL THEN 1 ELSE 0 END) FROM property')
    number1 = cursor.fetchone()
    print('количество не найденых ', number1[0])
    cursor.execute(
        'SELECT SUM(CASE WHEN found_address IS NULL THEN 0 ELSE 1 END) FROM property')
    number2 = cursor.fetchone()
    print('количество найденых ', number2[0])
    connection.commit()
    connection.close()
    return number1, number2


def mached_address():
    """
    Функция для определения количества объектов, для которых найденный адрес соответствует искомому
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT found_address FROM property INNER JOIN requests on requests.req_name = property.found_address')
    number = cursor.fetchone()
    print('number of similas addresses ', number)
    connection.commit()
    connection.close()
    return number


def main():
    chrome.maximize_window()  # увеличивает экран до максимального
    address = ""  # for storing input test
    create_requests_table()   # создаем таблицу для хранения результатов поиска
    create_search_table()    # создаем таблицу для хранения всех поисков
    # создаем список адресов для запросов
    requests = address_reader('test.csv')
    for address in requests:  # начинаем поиск по каждому из адресов
        # добавляем адрес поиска в таблицу для хранения всех поисков
        add_requests(address)
        cadast_num, found_address, cadast_link, full_json = get_data(address)
        if full_json == '':  # если по объекту результат не найден, будет возвращать объект
            k = 0  # обратно в поиск до трех раз. Если три попытки поиска подряд завершились неудачно,
            while k < 4:  # то больше не пытаемся его искать.
                # возвращаемся на главную страницу
                chrome.get("https://egrp365.ru/")
                cadast_num, found_address, cadast_link, full_json = get_data(
                    address)  # получаем результаты поиска
                k = k+1
        add_search_result(cadast_num, found_address,
                          cadast_link, full_json, address)  # добавляем результаты поиска в таблицу для хранения адресов для запросов
        chrome.get("https://egrp365.ru/")  # возвращаемся на главную страницу
    # определяем количество объектов, для которых найденный адрес соответствует искомому
    mached_address()
    # определить количество найденных и не найденных объектов.
    requests_notfound()


if __name__ == "__main__":  # tests
    main()
