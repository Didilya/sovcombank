from locators.quote_locators import QuoteLocators
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import json
from typing import Dict


class QuoteParser:
    """
    Given one of the specific quote divs, find out the data about
    the quote (quote content, author, tags).
    """

    def __init__(self, parent):
        self.parent = parent

    # def __repr__(self):
    def __repr__(self):
        diction = {self.content: self.author, 'link': self.tags}
        # print(diction)
        result = str(diction)
        #print(f'<name {self.content}, data {self.author}, link {self.tags}>')
        return result

    @ property
    def content(self):
        locator = QuoteLocators.CONTENT
        try:
            return self.parent.find_element_by_tag_name(locator).text
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass

    @ property
    def author(self):
        locator = QuoteLocators.AUTHOR
       # return self.parent.find_element_by_css_selector(locator).text
        try:
            return self.parent.find_element_by_tag_name(locator).text
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass

    @ property
    def tags(self):
        locator = QuoteLocators.TAGS
        try:
            return self.parent.find_element_by_css_selector(locator).get_attribute('href')
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass
