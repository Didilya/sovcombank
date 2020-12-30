from typing import List
from selenium.webdriver.support.ui import Select
import time
from locators.quotes_page_locators import QuotesPageLocators
from parsers.quote import QuoteParser
from bs4 import BeautifulSoup
import requests


class QuotesPage:
    def __init__(self, browser):
        self.browser = browser

    @property
    def quotes(self) -> List[QuoteParser]:
        # locator = QuotesPageLocators.QUOTE
        # quote_tags = self.soup.select(locator)
        # page_content = requests.get("https://egrp365.ru/").content
        html_list = self.browser.find_element_by_id("mapFlyout")
        items = html_list.find_elements_by_tag_name("li")
        # print(items)
        # for item in items:
        # text = item.text
        # print(text)
        #print([QuoteParser(e) for e in items])
        # self.browser.find_elements_by_css_selector(QuotesPageLocators.QUOTE)
        return [QuoteParser(e) for e in items]

    def data_search(self, address: str):
        element = self.browser.find_element_by_css_selector(
            QuotesPageLocators.ADDRESS)
        element.send_keys(address)
        element_b = self.browser.find_element_by_css_selector(
            QuotesPageLocators.SEARCH_BUTTON)
        element_b.click()

    def search_for_info(self, address) -> List[QuoteParser]:
        self.data_search(address)
        time.sleep(4)
        html_list = self.browser.find_element_by_id("mapFlyout")
        items = html_list.find_elements_by_tag_name("li")
        # new_list = [QuoteParser(e) for e in self.browser.find_elements_by_css_selector(
        # QuotesPageLocators.QUOTE)]
        time.sleep(3)
        return [QuoteParser(e) for e in items]
