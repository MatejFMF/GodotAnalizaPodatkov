import funkcije

url = "https://steamdb.info/charts"

with open("godot.html", "r", encoding="utf8") as file:
    godot_html = file.read()

godot_seznam = funkcije.findall_godot_games(godot_html)

funkcije.naredi_godot_csv("godot.csv", "id,naslov", godot_seznam)
