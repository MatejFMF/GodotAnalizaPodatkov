# GodotAnalizaPodatkov
Projektna naloga, v kateri iz podatkovne baze pridobimo in analiziramo podatke iger sprogramiranih v Godotu objavljene na portal Steam.

Seznam iger sem pridobil iz spletne strani https://steamdb.info/tech/Engine/Godot/,
podatke posamičnih iger pa sem pridobil iz spletne strani https://store.steampowered.com/.

### Navodila za uporabo:
* Naložimo zip na računalnik in ga ekstrahiramo
* Odpremo ekstrahiramo datoteko (priporočeno s programom Visual Studio Code).
* Za pridobitev podatkov zaženemo program main.py
* Za analizo podatkov odpremo datoteko analiza.ipynb
* Če vam program pravi, da nimate potrebnih knižnjic, jih morate naložiti z pip install
> Če se vam to zdi prezahtevno, si lahko samo pogledate datoteko analiza.ipynb

### Uporabljene knižnjice:
* re
* requests
* aiohttp
* asyncio
* pandas
* matplotlib.pyplot

#### Glede programa steam.py
steam.py je program, ki pregleda vse steam igre, vključen kot zanimiv dodatek.
Več informacij v [commit komentarju](https://github.com/MatejFMF/GodotAnalizaPodatkov/commit/9c240871379458a8541e99dd5c370fcc6475391f).