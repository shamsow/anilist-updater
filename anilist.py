import requests
import json
# Here we define our query as a multi-line string

def get_list_data(username="shamsow", userID=543014):
    """
    Query the AniList API for the users anime list
    """

    query = '''
    query ($page: Int, $perPage: Int, $user: String, $userID: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            mediaList (userId: $userID, userName: $user, status: COMPLETED) {
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

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    last_page = data["data"]["Page"]["pageInfo"]["lastPage"]


    for i in range(last_page):
        variables["page"] += 1
        response = requests.post(url, json={'query': query, 'variables': variables}).json()
        data["data"]["Page"]["mediaList"] += response["data"]["Page"]["mediaList"]
    
    print("Completed Shows in AniList:", len(data["data"]["Page"]["mediaList"]))

    return data

def create_anilist_file(output='anilist.json'):
    """
    Store the users anime list in a JSON file
    """
    data = get_list_data()

    with open(output, 'w') as f:
        json.dump(data, f)
    print("Created a new anilist file at:", output)
    return

def main():
    create_anilist_file()

if __name__ == "__main__":
    main()
