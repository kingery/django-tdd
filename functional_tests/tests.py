from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_start_list_and_retrieve(self):

        # Arvydas goes to the to-do list app web address
        self.browser.get(self.live_server_url)    # get http resource

        # Arvydas notices that the name "To-Do" is in the page title and header
        self.assertIn('To-Do', self.browser.title)        # browser attributes are of loaded page
        header_text = self.browser.find_element_by_tag_name('h1').text
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

        self.check_for_row_in_list_table('1: dunk on Shaq')

        # there is still a text box inviting him to enter another item. He enters "take a towel to the face"
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        input_box.send_keys('take a towel to the face')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page reloads and shows both items on the list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')    # tr for table record?
        self.check_for_row_in_list_table('1: dunk on Shaq')
        self.check_for_row_in_list_table('2: take a towel to the face')

        # He sees a special url and some instructions about how it will link back to this list
        self.fail("finish the test, ya dingus!")

        # Arvudas follows that link and sees his to-do list
