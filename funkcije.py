import csv
import os
import requests
import re


def download_url_to_string(url):
    return requests.get(url)


def findall_godot_games(html):
    vzorec = r'<a target="_blank" class="b" href="/app/(\d*)/">(.*)</a>'
    return [(x.group(1), x.group(2)) for x in re.finditer(vzorec, html)]


def naredi_godot_csv(datoteka, prva_vrstica, seznam):
    with open(datoteka, "w", encoding="utf8") as file:
        file.write(prva_vrstica + "\n")
        for igra in seznam:
            file.write(str(igra[0]) + "," + igra[1] + "\n")


class Igra:
    0

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return str((self.ime, "id: " + self.id))


def get_game_info(html):
    nova_igra = Igra()
    ime_vzorec = r'<div id="appHubAppName" class="apphub_AppName">(.*)</div>'
    nova_igra.ime = re.search(ime_vzorec, html).group(1)
    id_link_vzorec = (
        r'"og:url" content="(https://store.steampowered.com/app/(\d+).*)/">'
    )
    nova_igra.link = re.search(id_link_vzorec, html).group(1)
    nova_igra.id = re.search(id_link_vzorec, html).group(2)
    description_vzorec = r'"og:description" content="(.*)">'
    nova_igra.description = re.search(description_vzorec, html).group(1)
    developer_vzorec = r'<div class="summary column" id="developers_list">\s*<a href="https://store.steampowered.com/curator/.*">(.*)</a>'
    nova_igra.developer = re.search(developer_vzorec, html).group(1)
    publisher_vzorec = r'<div class="subtitle column">Publisher:</div>\s*<div class="summary column">\s*<a href="https://store.steampowered.com/curator/.*">(.*)</a>'
    nova_igra.publisher = re.search(publisher_vzorec, html).group(1)
    return nova_igra
