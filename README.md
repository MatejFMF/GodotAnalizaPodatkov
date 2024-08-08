# GodotAnalizaPodatkov
Projektna naloga, v kateri iz podatkovne baze pridobimo in analiziramo podatke iger sprogramiranih v Godotu objavljene na portal Steam.

Seznam iger sem pridobil iz spletne strani https://steamdb.info/tech/Engine/Godot/,
podatke posamičnih iger pa sem pridobil iz spletne strani https://store.steampowered.com/.

### Navodila za uporabo:
* Naložimo zip na računalnik in ga ekstrahiramo
* Odpremo ekstrahirano datoteko (priporočeno s programom Visual Studio Code).
* Za pridobitel podatkov zaženemo program main.py
* Za analizo podatkov odpremo datoteko analiza.ipynb
* Če vam program pravi, da nimate potrebnih knižnjic jih morate naložiti z pip install
> Če se vam to zdi prezahtevno, si lahko samo pogledate datoteko analiza.ipynb

### Uporabljene knižnijce:
* re
* requests
* aiohttp
* asyncio
* pandas
* matplotlib.pyplot