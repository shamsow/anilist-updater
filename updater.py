import json
import os
import colorama
import requests


from termcolor import cprint
from mal import create_mal_file
from anilist import create_anilist_file
from config import config_data

colorama.init()
DATA_FOLDER = 'data'
ANILIST_FILE = os.path.join(DATA_FOLDER, config_data.get("System", "anilist_file"))
MAL_FILE = os.path.join(DATA_FOLDER, config_data.get("System", "mal_file"))

statuses = {"Completed": "COMPLETED", "Watching": "CURRENT", "Plan to Watch": "PLANNING", "On-Hold": "PAUSED", "Dropped": "DROPPED"}

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def get_mediaId(idMal):
    query = """
        query ($id: Int, $type: MediaType) {
            Media (idMal: $id, type: $type) {
                id
                title {
                    english
                    romaji
                }
            }
        }
    """
    # Define our query variables and values that will be used in the query request
    variables = {
        "id": idMal,
        "type": "ANIME"
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables}).json()
    return (response["data"]["Media"]["id"], response["data"]["Media"]["title"]["english"])

def find_missing(anilist_file=ANILIST_FILE, mal_file=MAL_FILE):

    anilist = load_data(anilist_file)
    mal = load_data(mal_file)
    print("MyAnimeList file created on", mal["date"])

    # Get the id of all the anime in each list
    anilist_ids = {}
    for i in anilist["data"]["Page"]["mediaList"]:
        anilist_ids[i["media"]["idMal"]] = 1

    mal_id = list(map(int, mal["list_data"][0].keys()))

    # Find the anime that are in MAL but not in AniList
    missing_ids = []
    for id in mal_id:
        found = anilist_ids.get(id, None)
        if found is None:
            missing_ids.append((id, mal["list_data"][0][str(id)]["score"], mal["list_data"][0][str(id)]["status"]))

    cprint(f"Missing shows: {len(missing_ids)}", "yellow")
    # print(missing_ids)
    for id, _, _ in missing_ids:
        cprint(mal["list_data"][0][str(id)], "yellow")
    
    return missing_ids


def add_anime(id, score, status):
    mediaID, title = get_mediaId(id)
    print(f"Adding ID:{mediaID} [{title}] with a score of {score}")
    query = """
        mutation ($mediaId: Int, $status: MediaListStatus, $score: Float) {
        SaveMediaListEntry (mediaId: $mediaId, status: $status, score: $score) {
            id
            status
        }
    }
    """
    # Define our query variables and values that will be used in the query request
    variables = {
        "mediaId": mediaID,
        "status": statuses[status],
        "score": score
    }

    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': 'Bearer ' + config_data.get("Anilist", "ACCESS_TOKEN"),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers).json()
    # entry_id = response["data"]["SaveMediaListEntry"]["id"]
    cprint(f"Succesfully Added: ID:{mediaID}", "cyan")



def update_anilist(from_cli=True, refresh=False):
    if refresh:
        create_mal_file()
        create_anilist_file()
    missing = find_missing()
    if len(missing) > 0:
        if from_cli:
            command = input("Do you want to update your anilist? (y/n): ")
            if command == "y":
                print("Updating...")
                for id, score, status in missing:
                    add_anime(id, score, status)
        else:
            print("Updating...")
            for id, score, status in missing:
                add_anime(id, score, status)
    else:
        cprint("AniList is up to date with MyAnimeList", "cyan")     


if __name__ == "__main__":
    update_anilist(refresh=True)