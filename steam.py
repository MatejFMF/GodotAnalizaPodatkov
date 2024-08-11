import funkcije
import aiohttp
import asyncio
import re


steam_api = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

api = funkcije.download_url_to_string(steam_api)
steam_id_list = tuple(x for x in re.findall(r'"appid":(\d+),', api))


urls = [funkcije.id_to_link(id) for id in steam_id_list]


# S tema spremenljivkama nadzoriraš, kako hitro pridobivaš podatke
# Če je prehirto, lahko spletna stran zavrne
# cca. 3 ure, če ne pride do napak
request_time = 1
no_of_requests = 50

csv_size = 10000
zacetek = 1

###


async def fetch(session, url):
    async with session.get(url) as response:
        try:
            return await response.text()
        except:
            return "UTF-8 error"


async def main():
    csv = zacetek
    counter = 0
    for url_split in funkcije.split_tuple(urls, csv_size)[zacetek - 1 :]:
        with open(
            "Steam_podatki/steam" + f"{csv}" + ".csv",
            "w",
            encoding="utf8",
            errors="replace",
        ) as file:
            file.write(
                "id;ime;link;tip_aplikacije;cena;znižanje;datum_izdaje;izdajatelj;založnik;ocene;žanri;št_dosežkov;opis"
                + "\n"
            )
            stevilo_iger = len(urls)
            tasks: list = []
            async with aiohttp.ClientSession() as session:
                for url in url_split:
                    tasks.append(fetch(session, url))
                    counter += 1
                    if counter % no_of_requests == 0:
                        htmls = await asyncio.gather(*tasks)
                        for html in htmls:
                            igra = funkcije.get_game_info(html)
                            file.write(funkcije.game_info_to_string(igra) + "\n")
                            print(igra)
                        print(f"-- {counter}/{stevilo_iger} --")
                        tasks.clear()
                        await asyncio.sleep(request_time)
                htmls = await asyncio.gather(*tasks)
                for html in htmls:
                    igra = funkcije.get_game_info(html)
                    file.write(funkcije.game_info_to_string(igra) + "\n")
                    print(igra)
                print(f"-- {counter}/{stevilo_iger} --")
        csv += 1
        print("Making new csv file")
        await asyncio.sleep(request_time)

    print("-- Task complete --")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# Ta del kode je deloma prekopiran iz https://stackoverflow.com/a/50312981
