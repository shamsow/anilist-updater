import tkinter as tk
import requests
import time

from tkinter import font
# from bs4 import BeautifulSoup

from mal import create_mal_file, get_mal_data
from anilist import create_anilist_file, get_anilist_data
from updater import update_anilist, find_missing

# headers = requests.utils.default_headers()
# headers.update({
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
# })

# start = time.time()
# page = requests.get("https://9anime.to/schedule", headers = headers)
# x = time.time() - start
# spent = "{0:.3f}".format(x)
# print(f"Response received in {spent}s")

# def get_shows(day):
#     soup = BeautifulSoup(page.content, 'html.parser')
#     month = soup.find('span', class_='current').get_text()
#     content = soup.find('div', class_='content')
#     weekday = [i.get_text() for i in content.select('div.day-block div.head div.day')]
#     date = [i.get_text() for i in content.select('div.day-block div.head div.date')]
#     shows = [i for i in content.select('div.day-block div.items')]
#     items = []
#     for i in shows:
#         a = [x.get_text() for x in i.select('div.item div.info a.name')]
#         items.append(a)

#     try:
#         index = int(day) - 1
#         results = items[index]
#         text.delete(1.0, "end")
#         calendar = weekday[index] + ' ' + date[index] + ' ' + month
#         text.insert("insert", calendar + '\n')
#         for i in results:
#             text.insert("insert", i + '\n')
#     except:
#         text.delete(1.0, "end")
#         text.insert("insert", "INVALID DATE")


root = tk.Tk()
root.title("AniList Updater")

height = 800
width = 1500
theme = '#E0DEFF'
main = '#EEFEFF'


canvas = tk.Canvas(root, height=height, width=width, bg=main)
canvas.pack()

frame1 = tk.Text(root, bg=theme, bd=0)
frame1.place(relx=0.02, rely=0.1, relwidth=0.45, relheight=0.3)
scrollbar1 = tk.Scrollbar(frame1)
scrollbar1.pack(side='right', fill='y')

label1 = tk.Label(root, bg=theme, font=('Courier', 18), text="MyAnimeList")
label1.place(relwidth=0.45, relheight=0.05, relx=0.02, rely=0.04)

mal_data = get_mal_data()
date_mal = mal_data["date"]
completed_mal = mal_data["total_completed"]
frame1.insert("insert", f"List Date: {date_mal}\n")
frame1.insert("insert", f"Completed: {completed_mal}\n\n")
count = 1
for show in mal_data["list_data"][0].keys():
    title = mal_data["list_data"][0][show]["title"]
    frame1.insert("insert", f"{count}. {title}\n")
    count += 1
count = 1


frame2 = tk.Text(root, bg=theme, bd=0)
frame2.place(relx=0.53, rely=0.1, relwidth=0.45, relheight=0.3)
scrollbar2 = tk.Scrollbar(frame2)
scrollbar2.pack(side='right', fill='y')

label2 = tk.Label(root, bg=theme, font=('Courier', 18), text="AniList")
label2.place(relwidth=0.45, relheight=0.05, relx=0.53, rely=0.04)

anilist_data = get_anilist_data()
# print(anilist_data)
completed_anilist = anilist_data["data"]["Page"]["pageInfo"]["total"]
date_anilist = time.strftime("%Y-%m-%d")
frame2.insert("insert", f"List Date: {date_anilist}\n")
frame2.insert("insert", f"Completed: {completed_anilist}\n\n")
# anilist_titles = [i["media"]["title"]["english"] for i in  anilist["data"]["Page"]["mediaList"]]

for show in anilist_data["data"]["Page"]["mediaList"]:
    title = show["media"]["title"]["english"]
    if title is None:
        title = show["media"]["title"]["romaji"]
    frame2.insert("insert", f"{count}. {title}\n")
    count += 1


frame3 = tk.Text(root, bg=theme, bd=0)
frame3.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.45)

label3 = tk.Label(root, bg=theme, font=('Courier', 18), text="Missing shows")
label3.place(relwidth=0.96, relheight=0.05, relx=0.02, rely=0.44)

missing = find_missing()
for id, _, _ in missing:
    frame3.insert("insert", str(mal_data["list_data"][0][str(id)]) + "\n")
    # cprint(mal["list_data"][0][str(id)], "yellow")
# entry = tk.Entry(frame, bd=0, font=('Roman', 18), bg=main, highlightthickness=0)
# entry.place(relwidth=0.7, relheight=1)

# button = tk.Button(frame, text="Get Shows", bg="#FFDEED", bd=0, font=("Roman", 13), activebackground="#FFDEFD", command=lambda: get_shows(entry.get()))
# button.place(relx = 0.75, relwidth=0.25, relheight=1)

# frame2 = tk.Frame(root, bg=theme, bd=8)
# frame2.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.6)

# scrollbar = tk.Scrollbar(frame2)
# scrollbar.pack(side='right', fill='y')

# text = tk.Text(frame2, bg=main, bd=0, font=('Courier', 20), spacing1=5, padx=5, highlightthickness=0, yscrollcommand = scrollbar.set)
# text.place(relwidth=1, relheight=1)

root.resizable(0, 0)
root.mainloop()