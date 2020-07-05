import json
import requests

from mal import create_mal_file
from anilist import create_anilist_file

AUTH_FILE = 'auth.json'
ANILIST_FILE = 'anilist.json'
MAL_FILE = 'mal.json'

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def get_mediaId(idMal):
    query = """
        query ($id: Int) {
            Media (idMal: $id) {
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
        "id": idMal
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables}).json()
    return response["data"]["Media"]["id"]

def find_missing(anilist_file=ANILIST_FILE, mal_file=MAL_FILE):

    anilist = load_data(anilist_file)
    mal = load_data(mal_file)
    print("MyAnimeList file created on", mal["date"])

    anilist_id = [i["media"]["idMal"] for i in  anilist["data"]["Page"]["mediaList"]]
    print("Completed Shows in AniList:", len(anilist_id))

    mal_id = list(map(int, mal["list_data"][0].keys()))
    # print(mal_titles)

    missing_ids = []

    for id in mal_id:
        if id not in anilist_id:
            missing_ids.append((id, mal["list_data"][0][str(id)]["score"]))

    print("Missing shows:", len(missing_ids), missing_ids)

    for id, score in missing_ids:
        print(mal["list_data"][0][str(id)])
    
    # missing_ids = [idMal_to_mediaId[str(i)] for i in missing_ids]

    return missing_ids


def update_anilist(id, score):
    print(f"Adding ID:{id} with a score of {score}")
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
        "mediaId": get_mediaId(id),
        "status": "COMPLETED",
        "score": score
    }

    url = 'https://graphql.anilist.co'

    creds = {}
    with open(AUTH_FILE, 'r') as f:
        creds = json.load(f)

    headers = {
        'Authorization': 'Bearer ' + creds["ACCESS_TOKEN"],
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers).json()
    print("Added:", response["data"]["SaveMediaListEntry"]["id"])


def main():
    create_mal_file()
    create_anilist_file()
    missing = find_missing()
    if len(missing) > 0:
        command = input("Do you want to update your anilist? (y/n): ")
        if command == "y":
            print("Updating...")
            for id, score in missing:
                update_anilist(id, score)
    else:
        print("AniList is up to date with MyAnimeList")
        


if __name__ == "__main__":
    main()