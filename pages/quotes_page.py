from typing import List, Dict, Union
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from locators.quotes_page_locators import QuotesPageLocators
from parsers.quote import QuoteParser
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException

""" Данный модуль предназначен для скрецпинга информации с сайта   """


class QuotesPage:
    def __init__(self, browser):
        self.browser = browser

    @property
    def quotes(self) -> List[QuoteParser]:
        html_list = self.browser.find_element_by_id("mapFlyout")
        items = html_list.find_elements_by_tag_name("li")
        return [QuoteParser(e) for e in items]

    def data_search(self, address: str):
        """
        Функция для поиска веб-элементов и введение адреса в строку поиска
        """
        element = self.browser.find_element_by_css_selector(
            QuotesPageLocators.ADDRESS)   # поле для ввдода адреса поиска
        time.sleep(2)
        # передаем адресс в поле для ввдода адреса поиска
        element.send_keys(address)
        time.sleep(3)
        try:
            element_b = self.browser.find_element_by_css_selector(
                QuotesPageLocators.SEARCH_BUTTON)    # кнопка "Найти"
            time.sleep(3)
            # dropdown = self.browser.find_element_by_css_selector(
            # QuotesPageLocators.DROPDOWN14)
            # is = dropdown.find_elements(By.TAG_NAME, "div")

            dropdown14 = self.browser.find_element(
                By.XPATH, " /html/body/div[1]/div[2]/div[1]/div/div/div")  # элементы из выпадающего списка
            time.sleep(2)
            dropdown14.click()
            time.sleep(2)
            dropdown13 = self.browser.find_element(
                By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/a")  # элемент результата выпадающего списка
            time.sleep(2)
            dropdown13.click()

        except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException):
            print('one of ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException exeption')

    def search_for_info(self, address) -> Union[List[QuoteParser], str]:
        """
        Функция для получения списка значений результатов поиска, возвращает либо лист объектов QuoteParser или строку
        """
        self.data_search(
            address)  # запускает поиска веб-элементов и введение адреса в строку поиска
        time.sleep(2)
        list_info = []
        try:
            html_list = self.browser.find_element_by_id("mapFlyout")
            items = html_list.find_elements_by_tag_name("li")
            list_info = [QuoteParser(e) for e in items]
            if len(list_info) <= 0:
                other_format = self.browser.find_element_by_id(
                    "information_about_object")
                data = other_format.text
            return list_info
        except NoSuchElementException:
            print('NoSuchElementException raised by def search_for_inf')
        try:
            if len(list_info) <= 0:
                other_format = self.browser.find_element_by_id(
                    "information_about_object")
                data = other_format.text
                return data
        except NoSuchElementException:
            print('NoSuchElementException raised by def search_for_inf')
