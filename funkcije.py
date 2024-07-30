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
