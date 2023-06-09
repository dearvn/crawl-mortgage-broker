
import re, json, requests, math
from seleniumbase import BaseCase

BaseCase.main(__name__, __file__)


class LinkMortgageTest(BaseCase):
    def test_link_mortgage(self):

        self.open("https://findamortgagebroker.com/")

        address = '20001' # change this param
        current_page = 0 # change this param

        print("Start search:", address)
        self.type("input#contact-search-field", address['address'])
        self.click("button#contact-search-button")
        # stop to captcha manually first time
        self.sleep(30)

        if self.is_element_visible("div.no-results"):
            print(">>>>> NO RESULT")
            return

        if not self.is_element_visible("div#totalResults"):
            print("waiting div#totalResults ...................")
            self.sleep(3)

        total = self.get_text("div#totalResults").replace(" results", "")

        if int(total) == 0:
            return

        pages = int(math.ceil(int(total) / 20))

        print(">>>>>>>>>>total pages:", pages)

        if current_page == 0:
            source = self.get_page_source()

            section_open_tag = source.find('<section class="contact-search-results list-view" id="contactSearchResults">')
            section_close_tag = source.find('</section>', section_open_tag)
            everything_inside_section = source[section_open_tag + len(
                '<section class="contact-search-results list-view" id="contactSearchResults">'):section_close_tag]

            # save html to crawl link inside
            body = {'html': everything_inside_section, 'total': str(total), 'total_page': str(pages)}

        start = current_page
        if start == 0 or not start:
            start = 2

        for page in range(start, pages):
            if not self.is_element_visible("select#current-page"):
                print("waiting next page button ...................")
                self.sleep(3)
            print(">>>>> select page", page)
            self.select_option_by_text("select#current-page", str(page))

            self.sleep(3)

            source = self.get_page_source()

            section_open_tag = source.find(
                '<section class="contact-search-results list-view" id="contactSearchResults">')
            section_close_tag = source.find('</section>', section_open_tag)
            everything_inside_section = source[section_open_tag + len(
                '<section class="contact-search-results list-view" id="contactSearchResults">'):section_close_tag]

            # save html and current page to crawl link inside
            body = {'html': everything_inside_section, 'current_page': str(page+1)}

