import tkinter as tk
import requests
import time

from tkinter import font

from mal import create_mal_file, get_mal_data
from anilist import create_anilist_file, get_anilist_data
from updater import update_anilist, find_missing


HEIGHT = 800
WIDTH = 1500
THEME = '#e6ffff'
# THEME = '#a099ff'
MAIN = '#99e6ff'
# MAIN = '#EEFEFF'
BUTTON = '#99b3ff'
BUTTON_ACTIVE = '#809fff'

def update_frame(frame, content):
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

frame1 = tk.Text(root, bg=THEME, bd=0, font=('Arial', 18), spacing1=5, padx=5, highlightthickness=0)
frame1.place(relx=0.02, rely=0.1, relwidth=0.45, relheight=0.3)
label1 = tk.Label(root, bg=THEME, font=('System', 18), text="MyAnimeList")
label1.place(relwidth=0.45, relheight=0.05, relx=0.02, rely=0.04)
button1 = tk.Button(label1, text="Refresh", bg=BUTTON, bd=0, font=("Roman", 12), activebackground=BUTTON_ACTIVE, command=lambda: update_mal_frame(refresh=True))
button1.place(relx = 0.89, rely=0.1, relwidth=0.1, relheight=0.8)


frame2 = tk.Text(root, bg=THEME, bd=0, font=('Arial', 18), spacing1=5, padx=5, highlightthickness=0)
frame2.place(relx=0.53, rely=0.1, relwidth=0.45, relheight=0.3)
label2 = tk.Label(root, bg=THEME, font=('System', 18), text="AniList")
label2.place(relwidth=0.45, relheight=0.05, relx=0.53, rely=0.04)
button2 = tk.Button(label2, text="Refresh", bg=BUTTON, bd=0, font=("Roman", 12), activebackground=BUTTON_ACTIVE, command=lambda: update_anilist_frame(refresh=True))
button2.place(relx = 0.89, rely=0.1, relwidth=0.1, relheight=0.8)

frame3 = tk.Text(root, bg=THEME, bd=0, font=('Arial', 18), spacing1=5, padx=5, highlightthickness=0)
frame3.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.40)
label3 = tk.Label(root, bg=THEME, font=('System', 18), text="Missing shows")
label3.place(relwidth=0.96, relheight=0.05, relx=0.02, rely=0.44)
button3 = tk.Button(root, text="Update", bg=BUTTON, bd=0, font=("Roman", 14), activebackground=BUTTON_ACTIVE, command=lambda: update_anime())
button3.place(relx = 0.2, rely=0.92, relwidth=0.6, relheight=0.05)


def update_missing_frame():
    frame3.delete(1.0, "end")
    missing = find_missing()
    if len(missing) > 0:
        mal_data = get_mal_data()
        for id, _, _ in missing:
            frame3.insert("insert", str(mal_data["list_data"][0][str(id)]) + "\n")
    else:
        update_frame(frame3, "All MAL shows up to date with AniList")


def update_anime():
    
    update_anilist(from_cli=False)
    update_missing_frame()
    

def update_mal_frame(refresh=False):
    frame1.delete(1.0, "end")
    update_frame(frame1, "Refreshing...")
    if refresh:
        create_mal_file()
        update_missing_frame()
    frame1.delete(1.0, "end")
    mal_data = get_mal_data()
    date_mal = mal_data["date"]
    completed_mal = mal_data["total_completed"]
    update_frame(frame1, f"List Date: {date_mal}")
    update_frame(frame1, f"Completed: {completed_mal}\n")
    mal_titles = [mal_data["list_data"][0][show]["title"] for show in mal_data["list_data"][0]]
    update_frame(frame1, mal_titles)


def update_anilist_frame(refresh=False):
    frame2.delete(1.0, "end")
    update_frame(frame2, "Refreshing...")
    if refresh:
        create_anilist_file()
        update_missing_frame()
    frame2.delete(1.0, "end")
    anilist_data = get_anilist_data()
    completed_anilist = anilist_data["data"]["Page"]["pageInfo"]["total"]
    date_anilist = anilist_data["data"]["date"]
    update_frame(frame2, f"List Date: {date_anilist}")
    update_frame(frame2, f"Completed: {completed_anilist}\n")
    anilist_titles = []
    for show in anilist_data["data"]["Page"]["mediaList"]:
        title = show["media"]["title"]["english"]
        if title is None:
            title = show["media"]["title"]["romaji"]
        anilist_titles.append(title)
    update_frame(frame2, anilist_titles)
    

update_mal_frame()
update_anilist_frame()
update_missing_frame()

root.resizable(False, False)
root.mainloop()