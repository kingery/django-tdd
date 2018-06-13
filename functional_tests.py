from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_list_and_retrieve(self):

        # Arvydas goes to the to-do list app web address
        self.browser.get('http://localhost:8000')    # get http resource

        # Arvydas notices that the name "To-Do" is in the page title and header
        self.assertIn('To-Do', self.browser.title)        # browser attributes are of loaded page
        header_text = self.browser.find_element_by_tag_name('h1').txt
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item right away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "dunk on Shaq" into a text box
        input_box.send_keys('dunk on Shaq')

        # When he hits enter, the to-do list reloads and displays "1: dunk on Shaq"
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id list table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: dunk on Shaq' for row in rows)
        )

        # there is still a text box inviting him to enter another item. He enters "take a towel to the face"
        self.fail("finish the test, ya dingus!")

        # the page reloads and shows both items on the list

        # He sees a special url and some instructions about how it will link back to this list

        # Arvudas follows that link and sees his to-do list

if __name__ == '__main__':
        unittest.main(warnings='ignore')
