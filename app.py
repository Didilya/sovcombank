from selenium import webdriver
import time
from typing import Dict, Tuple, List, Union
import sqlite3
import json
from pages.quotes_page import QuotesPage


chrome = webdriver.Chrome(
    executable_path="/Users/BARAK/Desktop/sovcom/chromedriver.exe")
chrome.get("https://egrp365.ru/")
page = QuotesPage(chrome)

address = "г Казань, Зинина, 2"  # тестовый адрес



def get_data(address):   
    '''
    Функция для обработки полученных результатов скрейпинга
    Сохраняет нужные данные в переменные для передачи в БД
    '''
    scrapped_data = page.search_for_info(address)
    print(scrapped_data)
    full_json = ''
    for data in scrapped_data:
        new_data = str(data).replace('\'', '\"').replace(
            'None', '"None"')  # to convert to json

        res = json.loads(new_data)# создает в таблицу для хранения строк поиска
        print(res)

        if 'Почтовый адрес' in str(data):
            found_address = res['Почтовый адрес']
            print(found_address)
        else:
            found_address = None
        if 'Кадастровый номер дома' in str(data):
            draft_num = res['link']
            index = draft_num.find('=')+1
            end_index = len(draft_num)
            cadast_num = draft_num[index:end_index]
            print(cadast_num)
        else:
            cadast_num = None
        if 'Кадастровая карта' in str(data):
            cadast_link = res['link']
            print(cadast_link)
        else:
            cadast_link = None
        full_json = full_json + new_data  # to store full json request
    return cadast_num, found_address, cadast_link, full_json


def create_search_table():  # создает в таблицу для хранения результата поиска
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS property(idP integer primary key AUTOINCREMENT NOT NULL, cadast_num text, found_address text, cadast_link text, full_json text, request_address text NOT NULL, FOREIGN KEY(request_address) REFERENCES requests(req_name) ON DELETE CASCADE)')
    connection.commit()
    connection.close()


def create_requests_table(): # создает в таблицу для хранения строк поиска
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS requests(RequestsId integer primary key AUTOINCREMENT NOT NULL, req_name text NOT NULL)')
    connection.commit()
    connection.close()


def add_search_result(cadast_num, found_address, cadast_link, full_json, address): # добавить в таблицу результат поиска
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO property VALUES(NULL,?,?,?,?,?)',
                   (cadast_num, found_address, cadast_link, full_json, address))
    connection.commit()
    connection.close()


def add_requests(address):  # добавить в таблицу строку поиска
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO requests VALUES(NULL, ?)', (address,))
    connection.commit()
    connection.close()


# После получения результатов написать скрипты для следующего анализа:

def requests_notfound():  # определить количество найденных и не найденных объектов
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
   # cursor.execute('SELECT COUNT(found_address) FROM property WHERE ##found_address NOT IN(SELECT COUNT(DISTINCT found_address) FROM #property)')
    cursor.execute('SELECT COUNT (found_address) FROM property ')
    number = cursor.fetchone()
    print(number)
    connection.commit()
    connection.close()
    return number


def mached_address():  # определить количество объектов, для которых найденный адрес соответствует искомому
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
    create_requests_table()
    create_search_table()
    add_requests(address)
    cadast_num, found_address, cadast_link, full_json = get_data(address)
    add_search_result(cadast_num, found_address,
                      cadast_link, full_json, address)
    mached_address()
    requests_notfound()


main()
