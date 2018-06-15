from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 3

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_start_list_for_one_user(self):

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
        self.wait_for_row_in_list_table('1: dunk on Shaq')

        # there is still a text box inviting him to enter another item. He enters "take a towel to the face"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('take a towel to the face')
        input_box.send_keys(Keys.ENTER)

        # the page reloads and shows both items on the list
        self.wait_for_row_in_list_table('1: dunk on Shaq')
        self.wait_for_row_in_list_table('2: take a towel to the face')

        # satisfied, arvydas goes back to sleep


    def test_start_list_multiple_users_with_urls(self):
        
        # Arvydas starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('dunk on Shaq')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: dunk on Shaq')

        # he notices that the list has a unique url
        arvydas_list_url = self.browser.current_url
        self.assertRegex(arvydas_list_url, '/lists/.+')

        # now a new user, Jeff, comes along to make a list
        # he obviously is browsing in his own session...
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # jeff visits the home page, there is no sign of arvydas's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('dunk on Shaq', page_text)
        self.assertNotIn('take a towel to the face', page_text)

        # jeff enters his own items...
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('pick my nose')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: pick my nose')

        # jeff gets his own url
        jeff_list_url = self.browser.current_url
        self.assertRegex(jeff_list_url, '/lists/.+')
        self.assertNotEqual(jeff_list_url, arvydas_list_url)

        #  again there is no trace of arvydas's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('dunk on Shaq', page_text)
        self.assertNotIn('take a towel to the face', page_text)

        # satisfied they both go back to sleep
