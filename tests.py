import unittest
import json
import datetime
import os
import requests

# python3 -m unittest -v tests

class TestAccessToken(unittest.TestCase):
    def test_expiration(self):
        """
        Test that Access Token is still valid
        """
        
        filename = 'auth.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        expiration_date = datetime.datetime.strptime(data["EXPIRES"], "%Y-%m-%d")
        today_date = datetime.datetime.today()
        remaining = (expiration_date - today_date).days
        self.assertTrue(remaining > 0)


class TestSelenium(unittest.TestCase):
    def test_driver(self):
        """
        Check if the Chromedriver for selenium is properly configured
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chrome_path = os.path.join(BASE_DIR, ".anilist-venv", "bin", "chromedriver.exe")
        self.assertTrue(os.path.exists(chrome_path))


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