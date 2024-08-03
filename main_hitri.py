import funkcije
import aiohttp
import asyncio

with open("godot.html", "r", encoding="utf8") as file:
    godot_html = file.read()

godot_seznam = funkcije.findall_godot_games_ids(godot_html)

urls = [funkcije.id_to_link(id) for id in godot_seznam]


game_infos = []


# request_time določa, kako hitro program pošilja requeste
# manjši kot je čas, hitreje pošilja requeste
# če program prehitro pošilja pakete, ga bo spletna stran blokirala
request_time = 0.05
no_requests = 100


###


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    counter = 1
    stevilo_iger = len(urls)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
            await asyncio.sleep(request_time)
            print(f"Initating tasks: -- {counter}/{stevilo_iger} --")
            counter += 1
        counter = 1
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            igra = funkcije.get_game_info(html)
            game_infos.append(igra)
            print(igra, f"-- {counter}/{stevilo_iger} --")
            counter += 1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Ta del kode je večinoma prekopiran iz https://stackoverflow.com/a/50312981


print("-- Writing csv file... --")
with open("godot_hitro.csv", "w", encoding="utf8") as file:
    file.write(
        "id;ime;link;cena;discount;release_date;developer;publisher;all_reviews;genre;achievements;description"
        + "\n"
    )
    for game in game_infos:
        file.write(funkcije.game_info_to_string(game) + "\n")

print("-- Task complete --")
