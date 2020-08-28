import requests
import json
import os
import time

from config import config_data

ANILIST_FILE = config_data.get("System", "anilist_file")
USERNAME = config_data.get("Anilist", "username")
USER_ID = int(config_data.get("Anilist", "user_id"))

# Here we define our query as a multi-line string
def get_list_data(username=USERNAME, userID=USER_ID, status=""):
    """
    Query the AniList API for the users anime list
    """

    query = '''
    query ($page: Int, $perPage: Int, $user: String, $userID: Int, $status: MediaListStatus) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            mediaList (userId: $userID, userName: $user, status: $status) {
                score
                mediaId
                status
                media {
                idMal
                title {
                    english
                    romaji
                }
                }
                
                
            }
        }
    }
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        "userID": userID,
        "user": username,
        "page": 1,
        "perPage": 50
    }
    if status:
        variables["status"] = status
    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    last_page = data["data"]["Page"]["pageInfo"]["lastPage"]


    for _ in range(last_page):
        variables["page"] += 1
        response = requests.post(url, json={'query': query, 'variables': variables}).json()
        data["data"]["Page"]["mediaList"] += response["data"]["Page"]["mediaList"]
    
    print("AniList -> Completed:", data["data"]["Page"]["pageInfo"]["total"])

    return data

def create_anilist_file(output=ANILIST_FILE, directory='data'):
    """
    Store the users anime list in a JSON file
    """
    data = get_list_data(status="COMPLETED")
    data["data"]["date"] = time.strftime("%Y-%m-%d")
    with open(os.path.join(directory, output), 'w') as f:
        json.dump(data, f)
    print("Created a new anilist file at:", output)
    return


def get_anilist_data(filename=ANILIST_FILE, directory='data'):
    if os.path.exists(os.path.join(directory, filename)):
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)
        return data
    return "List JSON file not found"


def main():
    create_anilist_file()

if __name__ == "__main__":
    main()
