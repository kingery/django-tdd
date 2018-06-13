from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_list_and_retrieve(self):

        # Arvydas goes to the to-do list app web address
        self.browser.get('http://localhost:8000')    # get http resource

        # Arvydas notices that the name "To-Do" is in the page title
        self.assertIn('To-Do', self.browser.title)        # browser attributes are of loaded page
        self.fail("finish the test, ya dingus!")

        # He is invited to enter a to-do item right away

        # He types "dunk on Shaq" into a text box

        # When he hits enter, the to-do list reloads and displays "1: dunk on Shaq"

        # there is still a text box inviting him to enter another item. He enters "take a towel to the face"

        # the page reloads and shows both items on the list

        # He sees a special url and some instructions about how it will link back to this list

        # Arvudas follows that link and sees his to-do list

if __name__ == '__main__':
        unittest.main(warnings='ignore')
