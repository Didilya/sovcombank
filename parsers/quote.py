from locators.quote_locators import QuoteLocators
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import json
from typing import Dict

""" Данный модуль предназначен для парсинга полученной  информации с сайта   """


class QuoteParser:
    """
    Given one of the specific quote divs, find out the data about
    the quote (quote content, author, tags).
    """

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        diction = {self.content: self.author, 'link': self.tags}
        result = str(diction)

        return result

    @ property
    def content(self):
        locator = QuoteLocators.CONTENT
        try:
            return self.parent.find_element_by_tag_name(locator).text
        except NoSuchElementException:
            pass

    @ property
    def author(self):
        locator = QuoteLocators.AUTHOR

        try:
            return self.parent.find_element_by_tag_name(locator).text
        except NoSuchElementException:
            pass

    @ property
    def tags(self):
        locator = QuoteLocators.TAGS
        try:
            return self.parent.find_element_by_css_selector(locator).get_attribute('href')
        except NoSuchElementException:
            pass
