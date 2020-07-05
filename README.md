# MyAnimeList to AniList Updater

The idea behind this one is pretty simple:
I want to maintain a list on both MyAnimeList and AniList, but I don't want to make additions twice for each anime I watch.

## How it works

- This script will grab my list from MyAnimeList using `selenium` and MyAnimeList's handy export feature.
- I used `xml.etree.ElementTree` from Python's standard library to parse the xml list file.
- Dump the relevant list data in a `JSON` file.
- Use the AniList API to grab my list on AniList.
- Dump the relevant list data in a `JSON` file.
- Compare the two list `JSON` files to see what's missing on my AniList.
- Use the AniList API to update my list.

## Setup

The first thing needed is an access token from AniList to update your list. Head to [AniList](https://anilist.gitbook.io/anilist-apiv2-docs/overview/oauth/authorization-code-grant) to get it.

The second thing you need to add is our MAL username and password, this is needed to export your list.

Put the access token and your MAL credentials in an `auth.json` file in the project directory.

The file should look like so:
```
// auth.json
{
    "ACCESS_TOKEN": <your_access_token>,
    "MAL_USERNAME": <your_username>,
    "MAL_PASSWORD": <your_password>
}
```

After that, you need to setup your `selenium` driver. Download a chromedriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), place it somewhere convenient and note down the path to the driver.
Open up `mal.py` and update the `DRIVER_PATH` variale with your path.