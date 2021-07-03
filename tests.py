import unittest
import datetime
import os
import requests

from config import config_data
from selenium import webdriver
from mal import DRIVER_PATH
from selenium.common.exceptions import NoSuchElementException
# python -m unittest -v tests

class TestAccessToken(unittest.TestCase):
    def test_expiration(self):
        """
        Test that Access Token is still valid
        """
        expiration_date = datetime.datetime.strptime(config_data.get("Anilist", "EXPIRES"), "%Y-%m-%d")
        today_date = datetime.datetime.today()
        remaining = (expiration_date - today_date).days
        self.assertTrue(remaining > 0)


class TestInternet(unittest.TestCase):
    def test_ping_google(self):
        """
        Test the internet connection by pinging Google
        """
        req = requests.get("https://google.com")
        self.assertEqual(req.status_code, 200)
    

class TestSelenium(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # chrome_path = os.path.join(BASE_DIR, DRIVER_PATH)
    chrome_path = DRIVER_PATH

    def setUp(self):
        """
        Setup the chrome webdriver
        """
        self.driver = webdriver.Chrome(executable_path=self.chrome_path)
    
    def test_driver(self):
        """
        Check if the Chromedriver for selenium is properly configured
        """
        self.assertTrue(os.path.exists(self.chrome_path))
   
    def test_mal_login_button(self):
        """
        Check if the login button on MAL can be found by known methods
        """
        driver = self.driver
        driver.get("https://myanimelist.net/login.php")
        res = []
        # Test method 1
        try:
            driver.find_element_by_name("Login")
            res.append(True)
        except NoSuchElementException:
            res.append(False)
        # Test method 2
        try:
            driver.find_element_by_css_selector('input.inputButton.btn-form-submit.btn-recaptcha-submit')
            res.append(True)
        except:
            res.append(False)
        # Passes if either method works
        self.assertTrue(any(res))

    def tearDown(self):
        self.driver.close()


class TestAnilistAPI(unittest.TestCase):
    def test_connection(self):
        """
        Test the Anilist API with a simple query
        """
        query = '''
        query ($id: Int) {
            Media (id: $id) {
                id
                title {
                    english
                }
            }
        }
        '''

        # Define our query variables and values that will be used in the query request
        variables = {
            "id": 1
        }

        url = 'https://graphql.anilist.co'

        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables}).json()
        self.assertEqual(response["data"]["Media"]["title"]["english"], "Cowboy Bebop")


if __name__ == '__main__':
    unittest.main()