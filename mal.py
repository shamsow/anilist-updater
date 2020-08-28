import os
import json
import time
import shutil
import gzip
import fire
import requests
import xml.etree.ElementTree as ET

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import config_data
from glob import glob


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join("/mnt", "c", "Users", "Sadat", "Downloads" + os.sep)
PROJECT_DIR = os.path.join(BASE_DIR, "src" + os.sep)
DATA_FOLDER = 'data'
DATA_DIR = os.path.join(BASE_DIR, 'src', 'data' + os.sep)
DRIVER_PATH = os.path.join(BASE_DIR, ".anilist-venv", "bin", "chromedriver.exe")
MAL_FILE = config_data.get("System", "mal_file")
MAL_XML_FILE = config_data.get("System", "mal_xml_file")

def fetch_list(download_location=DOWNLOAD_DIR, desired_location=DATA_DIR, check_date=False):
    """
    Use Selenium with a Chrome driver to get the MyAnimeList xml file and move it to the project folder
    """
    # Check if internet connection works
    req = requests.get("https://google.com")
    if req.status_code != 200:
        print("No internet. Can't fetch new list.")
        return
    
    if check_date:
        # Check if list has already been fetched today
        if os.path.exists(DATA_DIR + MAL_FILE):
            with open(DATA_DIR + MAL_FILE, 'r') as f:
                data = json.load(f)
            if data["date"] == time.strftime("%Y-%m-%d"):
                print("List already fetched today, proceed with present list file.")
                return
            print("List outdated")
    print("Fetching list from MyAnimeList")
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {
    #     "download.default_directory" :  BASE_DIR,
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    chrome_path = DRIVER_PATH
    # driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    driver = webdriver.Chrome(executable_path=chrome_path)

    driver.get("https://myanimelist.net/login.php")
    # Get MAL username and password
    username, password = config_data.get("MAL", "username"), config_data.get("MAL", "password")
    driver.find_element_by_id("loginUserName").send_keys(username)
    driver.find_element_by_id("login-password").send_keys(password)
    # driver.find_element_by_name("Login").click()
    driver.find_element_by_css_selector('input.inputButton.btn-form-submit.btn-recaptcha-submit').click()
    # Navigate to list export page accept the alert
    time.sleep(1)
    driver.get("https://myanimelist.net/panel.php?go=export")
    time.sleep(1)
    elem = driver.find_element_by_name("subexport")
    elem.click()
    alert = driver.switch_to.alert
    alert.accept()
    # Get the current page after being redirected
    new_url = driver.window_handles[0]
    driver.switch_to.window(new_url)
    time.sleep(0.5)
    # Click the list export link and download
    list_link = driver.find_element_by_partial_link_text("animelist_")
    list_link.click()
    # Delay for 5 seocnds to allow the list to donwload
    time.sleep(3)
    print("Selenium tasks complete")
    driver.close()

    print("Copying file")
    # Get the downloaded file from the downloads folder and move it to project folder
    filename = glob(download_location + '*.gz')
    if len(filename) == 0:
        return
    elif len(filename) > 1:
        print("More than one animelist .gz files in donwloads folder. Delete all except the latest one. Files found:", filename)
        return
    print(desired_location + filename[0][29:])
    with open(filename[0], 'rb') as f_in:
        
        with open(desired_location + filename[0][29:], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename[0])

    return True


def unzip_list():
    """
    Unzip the animelist .gz file in the project directory and remove the zip file
    """
    print("Unzipping list file")
    filename = glob(os.path.join(DATA_FOLDER, '*.gz'))
    if len(filename) == 0:
        print("No .gz animelist files found. Extraction not needed.")
        return
    if len(filename) > 1:
        print("More than one .gz file in the project folder. Delete all except the latest one. Files found:", filename)
        return
    
    with gzip.open(filename[0], 'rb') as f_in:
        with open(filename[0][:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename[0])


def rename_list(new_name=MAL_XML_FILE):
    """
    Rename the animelist xml file in project folder to preset value
    """
    unzip_list()

    print("Renaming new list and removing old one")
    xml_file = glob(os.path.join(DATA_FOLDER, '*.xml'))
    if len(xml_file) > 1:
        print(xml_file)
        for name in xml_file:
            # Remove the old animelist file
            if name[len(DATA_FOLDER) + 1:] == MAL_XML_FILE: # Use string indexing to compare the filenames only
                os.remove(name)
        xml_file = glob(os.path.join(DATA_FOLDER, '*.xml'))
        print(xml_file)
    # Rename the latest animelist file
    os.rename(xml_file[0], os.path.join(DATA_FOLDER, new_name))

def extract_data_from_list(filename, completed_only=True):
    """
    Extract the relevant anime data from the animelist xml file
    """
    rename_list()

    print("Extracting data from list xml file")
    if not os.path.exists(os.path.join(DATA_FOLDER, filename)):
        print("Could not find the list file. Make sure the file has been added and properly named.")
        return

    # Get the needed user info fields from the xml file
    tree = ET.parse(os.path.join(DATA_FOLDER, filename))
    root = tree.getroot()
    info = root[0]
    username = info.find('user_name').text
    total_anime = info.find('user_total_anime').text
    total_completed = info.find('user_total_completed').text
    date = time.strftime("%Y-%m-%d")
    data = {"username": username, "total_anime": total_anime, "total_completed": total_completed, "date": date, "list_data": []}

    # Get the needed anime info fields form the xml file
    anime = {}
    for child in root[1:]:
        title = child.find('series_title').text
        score = child.find('my_score').text
        status = child.find('my_status').text
        malID = child.find('series_animedb_id').text
        watched_episodes = child.find('my_watched_episodes').text
        if completed_only:
            if status == "Completed":
                anime[malID] = {'title': title, 'score': score, 'status': status, 'watched_episodes': watched_episodes}
        else:
            anime[malID] = {'title': title, 'score': score, 'status': status, 'watched_episodes': watched_episodes}
    
    print(f"MyAnimeList -> Total: {total_anime}, Completed: {total_completed}")

    data["list_data"].append(anime)
    
    return data


def create_mal_file(filename=MAL_XML_FILE, output=MAL_FILE):
    """
    Store the relevant anime data from the xml file in a JSON file
    """
    fetch_list(check_date=True)
    # if res is not None:
        # Proceed to creating a file if the old one is invalid or it doesn't exist
    data = extract_data_from_list(filename)
    if data is not None:
        with open(os.path.join(DATA_FOLDER, output), 'w') as f:
            json.dump(data, f)
        print("Created a new MyAnimeList file at:", output)
        return


def get_mal_data(filename=MAL_FILE):
    """
    Returns the MAL data saved in a JSON file if it exists
    """
    if os.path.exists(os.path.join(DATA_FOLDER, filename)):
        with open(os.path.join(DATA_FOLDER, filename), 'r') as f:
            data = json.load(f)
        return data
    return "List JSON file not found"


def main():
    # create_mal_file()
    print("Usage: python3 mal.py [command]")
    print("Commands reference: python3 mal.py -- --help")
    fire.Fire({
        'create': create_mal_file,
        'fetch': fetch_list,
        'rename': rename_list,
        'unzip': unzip_list,
    })
    

if __name__ == '__main__':
    main()
