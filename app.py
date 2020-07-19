import tkinter as tk
import requests
import time

from tkinter import font
# from bs4 import BeautifulSoup

from mal import create_mal_file, get_mal_data
from anilist import create_anilist_file, get_anilist_data
from updater import update_anilist, find_missing


HEIGHT = 800
WIDTH = 1500
THEME = '#E0DEFF'
MAIN = '#EEFEFF'

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

def update_frame(frame, content):
    # frame.insert("insert", content)
    if isinstance(content, list):
        content = enumerate(content)
        for i, line in content:
            frame.insert("insert", f"{i+1}. {line}\n")
    else:
        frame.insert("insert", f"{content}\n")

root = tk.Tk()
root.title("AniList Updater")




canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=MAIN)
canvas.pack()

frame1 = tk.Text(root, bg=THEME, bd=0)
frame1.place(relx=0.02, rely=0.1, relwidth=0.45, relheight=0.3)
# scrollbar1 = tk.Scrollbar(frame1)
# scrollbar1.pack(side='right', fill='y')
label1 = tk.Label(root, bg=THEME, font=('Courier', 18), text="MyAnimeList")
label1.place(relwidth=0.45, relheight=0.05, relx=0.02, rely=0.04)
button1 = tk.Button(label1, text="Refresh", bg="#FFDEED", bd=0, font=("Roman", 10), activebackground="#FFDEFD", command=lambda: update_mal_frame(refresh=True))
button1.place(relx = 0.9, rely=0.1, relwidth=0.1, relheight=0.8)


frame2 = tk.Text(root, bg=THEME, bd=0)
frame2.place(relx=0.53, rely=0.1, relwidth=0.45, relheight=0.3)
# scrollbar2 = tk.Scrollbar(frame2)
# scrollbar2.pack(side='right', fill='y')
label2 = tk.Label(root, bg=THEME, font=('Courier', 18), text="AniList")
label2.place(relwidth=0.45, relheight=0.05, relx=0.53, rely=0.04)
button2 = tk.Button(label2, text="Refresh", bg="#FFDEED", bd=0, font=("Roman", 10), activebackground="#FFDEFD", command=lambda: update_anilist_frame(refresh=True))
button2.place(relx = 0.9, rely=0.1, relwidth=0.1, relheight=0.8)

frame3 = tk.Text(root, bg=THEME, bd=0)
frame3.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.40)
label3 = tk.Label(root, bg=THEME, font=('Courier', 18), text="Missing shows")
label3.place(relwidth=0.96, relheight=0.05, relx=0.02, rely=0.44)
button3 = tk.Button(root, text="Update", bg="#FFDEED", bd=0, font=("Roman", 10), activebackground="#FFDEFD", command=lambda: print("update button clicked"))
button3.place(relx = 0.2, rely=0.92, relwidth=0.6, relheight=0.05)

def update_missing_frame():
    frame3.delete(1.0, "end")
    missing = find_missing()
    # missing = map(str, missing)
    # missing_shows = [str(mal_data["list_data"][0][str(id)]) for id in missing]
    # update_frame(frame3, missing_shows)
    mal_data = get_mal_data()
    for id, _, _ in missing:
        frame3.insert("insert", str(mal_data["list_data"][0][str(id)]) + "\n")


def update_mal_frame(refresh=False):
    frame1.delete(1.0, "end")
    update_frame(frame1, "Refreshing...")
    if refresh:
        create_mal_file()
    frame1.delete(1.0, "end")
    mal_data = get_mal_data()
    date_mal = mal_data["date"]
    completed_mal = mal_data["total_completed"]
    # frame1.insert("insert", f"List Date: {date_mal}\n")
    # frame1.insert("insert", f"Completed: {completed_mal}\n\n")
    update_frame(frame1, f"List Date: {date_mal}")
    update_frame(frame1, f"Completed: {completed_mal}\n")
    mal_titles = [mal_data["list_data"][0][show]["title"] for show in mal_data["list_data"][0]]
    # for show in mal_data["list_data"][0].keys():
    #     title = mal_data["list_data"][0][show]["title"]
    #     frame1.insert("insert", f"{count}. {title}\n")
    #     count += 1
    update_frame(frame1, mal_titles)
    update_missing_frame()
# count = 1

def update_anilist_frame(refresh=False):
    frame2.delete(1.0, "end")
    update_frame(frame2, "Refreshing...")
    if refresh:
        create_anilist_file()
    frame2.delete(1.0, "end")
    anilist_data = get_anilist_data()
    # print(anilist_data)
    completed_anilist = anilist_data["data"]["Page"]["pageInfo"]["total"]
    date_anilist = anilist_data["data"]["date"]
    # frame2.insert("insert", f"List Date: {date_anilist}\n")
    update_frame(frame2, f"List Date: {date_anilist}")
    update_frame(frame2, f"Completed: {completed_anilist}\n")
    # frame2.insert("insert", f"Completed: {completed_anilist}\n\n")
    # anilist_titles = [show["media"]["title"]["english"] if show["media"]["title"]["english"] else show["media"]["title"]["romaji"] for show in  anilist_data["data"]["Page"]["mediaList"]]
    anilist_titles = []
    for show in anilist_data["data"]["Page"]["mediaList"]:
        title = show["media"]["title"]["english"]
        if title is None:
            title = show["media"]["title"]["romaji"]
        anilist_titles.append(title)
    update_frame(frame2, anilist_titles)
    update_missing_frame()

update_mal_frame()
update_anilist_frame()





# entry = tk.Entry(frame, bd=0, font=('Roman', 18), bg=MAIN, highlightthickness=0)
# entry.place(relwidth=0.7, relheight=1)

# button = tk.Button(frame, text="Get Shows", bg="#FFDEED", bd=0, font=("Roman", 13), activebackground="#FFDEFD", command=lambda: get_shows(entry.get()))
# button.place(relx = 0.75, relwidth=0.25, relheight=1)

# frame2 = tk.Frame(root, bg=THEME, bd=8)
# frame2.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.6)

# scrollbar = tk.Scrollbar(frame2)
# scrollbar.pack(side='right', fill='y')

# text = tk.Text(frame2, bg=MAIN, bd=0, font=('Courier', 20), spacing1=5, padx=5, highlightthickness=0, yscrollcommand = scrollbar.set)
# text.place(relwidth=1, relheight=1)

root.resizable(False, False)
root.mainloop()