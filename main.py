import funkcije
import aiohttp
import asyncio

with open("godot.html", "r", encoding="utf8") as file:
    godot_html = file.read()

godot_seznam = funkcije.findall_godot_games_ids(godot_html)

urls = [funkcije.id_to_link(id) for id in godot_seznam]


# S tema spremenljivkama nadzoriraš, kako hitro pridobivaš podatke
# Če je prehirto, lahko spletna stran zavrne
# cca. 5 minut
request_time = 1
no_of_requests = 20


###


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    with open("godot.csv", "w", encoding="utf8") as file:
        file.write(
            "id;ime;link;app_type;cena;discount;release_date;developer;publisher;all_reviews;genre;achievements;description"
            + "\n"
        )
        counter = 0
        stevilo_iger = len(urls)
        tasks: list = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Ta del kode je deloma prekopiran iz https://stackoverflow.com/a/50312981


print("-- Task complete --")
