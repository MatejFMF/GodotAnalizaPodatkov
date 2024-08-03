import requests
import re


def download_url_to_string(url):
    return requests.get(url).text


def findall_godot_games_ids(html):
    vzorec = r'<a target="_blank" class="b" href="/app/(\d*)/">(.*)</a>'
    return tuple(x.group(1) for x in re.finditer(vzorec, html))


def naredi_godot_csv(datoteka, prva_vrstica, seznam):
    with open(datoteka, "w", encoding="utf8") as file:
        file.write(prva_vrstica + "\n")
        for igra in seznam:
            file.write(str(igra[0]) + "," + igra[1] + "\n")


class Igra:

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Id: {self.id}, {self.ime}"


def remove_semicolon(niz):
    niz = niz.replace("amp;", "")
    niz = niz.replace("&quot;", '"')
    niz = niz.replace(";", ":,")
    return niz


def find_information(vzorec, html, group_number, not_found_message="None"):
    try:
        return remove_semicolon(re.search(vzorec, html).group(group_number))
    except:
        return not_found_message


def find_multiple_information(vzorec, html, group_numbers, not_found_message="None"):
    try:
        return remove_semicolon(str(re.search(vzorec, html).group(*group_numbers)))
    except:
        return not_found_message


def find_all_information(vzorec, html, not_found_message="None"):
    try:
        return remove_semicolon(str(tuple(x for x in re.findall(vzorec, html))))
    except:
        return not_found_message


# VZORCI
ime_vzorec = r'<div id="appHubAppName" class="apphub_AppName">(.*)</div>'
id_link_vzorec = r'"og:url" content="(https://store.steampowered.com/app/(\d+).*)/">'
cena_vzorec1 = r'<div class="discount_block game_purchase_discount.*?data-bundlediscount="0".*?aria-label="(\d*%) off. (.*?) normally, discounted to (.*?)">'
cena_vzorec2 = r'<div class="game_purchase_price price" data-price-final="\d*">\n*?\s*(.*?)\s*</div>'
developer_vzorec = r'<div class="summary column" id="developers_list">\n?\s*<a href="https://store.steampowered.com/.*">(.*)</a>'
publisher_vzorec = r'<div class="subtitle column">Publisher:</div>\n?\s*<div class="summary column">\n?\s*<a href="https://store.steampowered.com/.*">(.*)</a>'
release_date_vzorec = r"<b>Release Date:</b> (.*)<br>"
all_reviews_vzorec = r'<div class="subtitle column all">All Reviews:</div>\n?\s*<div class="summary column">\n?\s*<span class=.*>(.*)</span>\n?\s*<span class="responsive_hidden">\n?\s*\((.*)\)\n?\s*</span>\n?\s*<span class="nonresponsive_hidden responsive_reviewdesc">\n?\s*- (\d+%)'
recent_reviews_vzorec = r'<div class="subtitle column">Recent Reviews:</div>\n?\s*<div class="summary column">\n?\s*<span class=.*>(.*)</span>\n?\s*<span class="responsive_hidden">\n?\s*\((.+)\)\n?\s*</span>\n?\s*<span class="nonresponsive_hidden responsive_reviewdesc">\n\s*- (\d+%)'
genre_vzorec = r'<a href="https://store.steampowered.com/genre/.*?">(.*?)</a>[,<]'
achievements_vzorec = r'<div class="responsive_banner_link_title responsive_chevron_right">View Steam Achievements <span class="responsive_banner_link_total">\((\d*)\)</span></div>'
description_vzorec = r'"og:description" content="(.*)">'


def get_game_info(html):
    nova_igra = Igra()
    nova_igra.ime = find_information(ime_vzorec, html, 1)
    nova_igra.link = find_information(id_link_vzorec, html, 1)
    nova_igra.id = find_information(id_link_vzorec, html, 2)
    nova_igra.cena = find_information(cena_vzorec1, html, 2, "not_found")
    if nova_igra.cena == "not_found":
        nova_igra.cena = find_information(cena_vzorec2, html, 1, "Free")
    nova_igra.discount = find_multiple_information(
        cena_vzorec1, html, (1, 3), "No discount"
    )
    nova_igra.developer = find_information(developer_vzorec, html, 1)
    nova_igra.publisher = find_information(publisher_vzorec, html, 1)
    nova_igra.release_date = find_information(release_date_vzorec, html, 1)
    nova_igra.all_reviews = find_multiple_information(
        all_reviews_vzorec, html, (1, 2, 3), "No reviews"
    )
    nova_igra.genre = find_all_information(genre_vzorec, html)
    nova_igra.achievements = find_information(
        achievements_vzorec, html, 1, "No achievements"
    )
    nova_igra.description = find_information(description_vzorec, html, 1)
    return nova_igra


def id_to_link(id):
    return "https://store.steampowered.com/app/" + str(id)


def game_info_to_string(igra: Igra):
    return f"{igra.id};{igra.ime};{igra.link};{igra.cena};{igra.discount};{igra.release_date};{igra.developer};{igra.publisher};{igra.all_reviews};{igra.genre};{igra.achievements};{igra.description}"
