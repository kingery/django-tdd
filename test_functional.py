from selenium import webdriver

browser = webdriver.Firefox()           # create browser object
browser.get('http://localhost:8000')    # get http resource

assert 'Django' in browser.title        # browser attributes are of loaded page
