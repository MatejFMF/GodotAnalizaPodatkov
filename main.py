import funkcije

steam_url = "https://store.steampowered.com/search/?ignore_preferences=1"

with open("godot.html", "r", encoding="utf8") as file:
    godot_html = file.read()

godot_seznam = funkcije.findall_godot_games(godot_html)


with open("godot.csv", "w", encoding="utf8") as file:
    file.write(
        "id;ime;link;cena;discount;release_date;developer;publisher;all_reviews;genre;achievements;description;"
        + "\n"
    )
    for igra in godot_seznam:
        url: str = funkcije.id_to_link(igra[0])
        html: str = funkcije.download_url_to_string(url)
        game_info = funkcije.get_game_info(html)
        print(game_info)
        file.write(funkcije.game_info_to_string(game_info) + "\n")
    print("Task complete.")
