import csv
import os
import requests
import re


def download_url_to_string(url):
    return requests.get(url).text


def findall_godot_games(html):
    vzorec = r'<a target="_blank" class="b" href="/app/(\d*)/">(.*)</a>'
    return ((x.group(1), x.group(2)) for x in re.finditer(vzorec, html))


def naredi_godot_csv(datoteka, prva_vrstica, seznam):
    with open(datoteka, "w", encoding="utf8") as file:
        file.write(prva_vrstica + "\n")
        for igra in seznam:
            file.write(str(igra[0]) + "," + igra[1] + "\n")


class Igra:

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return str((self.ime, "id: " + self.id))


def get_game_info(html):
    nova_igra = Igra()
    ime_vzorec = r'<div id="appHubAppName" class="apphub_AppName">(.*)</div>'
    try:
        nova_igra.ime = re.search(ime_vzorec, html).group(1)
    except:
        nova_igra.ime = "None"
    id_link_vzorec = (
        r'"og:url" content="(https://store.steampowered.com/app/(\d+).*)/">'
    )
    try:
        nova_igra.link = re.search(id_link_vzorec, html).group(1)
    except:
        nova_igra.link = "None"
    try:
        nova_igra.id = re.search(id_link_vzorec, html).group(2)
    except:
        nova_igra.id = "None"
    developer_vzorec = r'<div class="summary column" id="developers_list">\n?\s*<a href="https://store.steampowered.com/.*">(.*)</a>'
    try:
        nova_igra.developer = re.search(developer_vzorec, html).group(1)
    except:
        nova_igra.vzorec = "None"
    publisher_vzorec = r'<div class="subtitle column">Publisher:</div>\n?\s*<div class="summary column">\n?\s*<a href="https://store.steampowered.com/.*">(.*)</a>'
    try:
        nova_igra.publisher = re.search(publisher_vzorec, html).group(1)
    except:
        nova_igra.publisher = "None"
    release_date_vzorec = r"<b>Release Date:</b> (.*)<br>"
    try:
        nova_igra.release_date = re.search(release_date_vzorec, html).group(1)
    except:
        nova_igra.vzorec = "None"
    recent_reviews_vzorec = r'<div class="subtitle column">Recent Reviews:</div>\n?\s*<div class="summary column">\n?\s*<span class=.*>(.*)</span>\n?\s*<span class="responsive_hidden">\n?\s*\((.+)\)\n?\s*</span>\n?\s*<span class="nonresponsive_hidden responsive_reviewdesc">\n\s*- (\d+%)'
    try:
        nova_igra.recent_reviews = str(
            re.search(recent_reviews_vzorec, html).group(1, 2, 3)
        )
    except:
        nova_igra.recent_reviews = "None"
    all_reviews_vzorec = r'<div class="subtitle column all">All Reviews:</div>\n?\s*<div class="summary column">\n?\s*<span class=.*>(.*)</span>\n?\s*<span class="responsive_hidden">\n?\s*\((.*)\)\n?\s*</span>\n?\s*<span class="nonresponsive_hidden responsive_reviewdesc">\n?\s*- (\d+%)'
    try:
        nova_igra.all_reviews = str(re.search(all_reviews_vzorec, html).group(1, 2, 3))
    except:
        nova_igra.all_reviews = "None"
    genre_vzorec = r'<a href="https://store.steampowered.com/genre/.*?">(.*?)</a>'
    try:
        nova_igra.genre = str(tuple(x for x in re.findall(genre_vzorec, html)))
    except:
        nova_igra.genre = "None"
    achievements_vzorec = r'<div class="responsive_banner_link_title responsive_chevron_right">View Steam Achievements <span class="responsive_banner_link_total">\((\d*)\)</span></div>'
    try:
        nova_igra.achievements = re.search(achievements_vzorec, html).group(1)
    except:
        nova_igra.achievements = "0"
    description_vzorec = r'"og:description" content="(.*)">'
    try:
        nova_igra.description = re.search(description_vzorec, html).group(1)
    except:
        nova_igra.description = "None"
    return nova_igra


def id_to_link(id):
    return "https://store.steampowered.com/app/" + str(id)


def game_info_to_string(igra: Igra):
    return f"{igra.id};{igra.ime};{igra.link};{igra.release_date};{igra.developer};{igra.publisher};{igra.recent_reviews};{igra.all_reviews};{igra.genre};{igra.achievements};{igra.description}"
