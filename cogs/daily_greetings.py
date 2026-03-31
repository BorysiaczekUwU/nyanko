import discord
from discord.ext import commands, tasks
import random
import datetime

MORNING_MESSAGES = [
    "Dzień dobry! Słoneczko już wstało, czas zacząć nowy dzień! ☀️",
    "Pobudka! Kawa zaparzona, można podbijać świat! ☕",
    "Otwieramy oczka! Niech ten dzień będzie dla Was wspaniały! 🌸",
    "Dobrego ranka! Mam nadzieję, że spaliście smacznie. 🛌",
    "Czas wstać i błyszczeć! Wspaniałego dnia! ✨",
    "Dzień dobry w ten piękny poranek. Pamiętajcie o uśmiechu! 😊",
    "Nowy dzień, nowe możliwości! Trzymam za Was kciuki. 🤞",
    "Pieski poszczały, ptaszki ćwierkają - wstawajcie! 🐦",
    "Kto wcześnie wstaje, ten... jest zaspanym kotkiem. Dzień dobry! 😺",
    "Witamy w nowym, wspaniałym dniu! Głowa do góry! 🌈",
    "Oby kawa dzisiaj smakowała wyjątkowo dobrze. Dzień dobry! ☕",
    "Cześć i czołem! Wyskakujcie z łóżek, szkoda dnia! 🏃‍♂️",
    "Słodkiego poranka i udanego całego dnia życzy wasz bot! 🍬",
    "Pamiętaj, że każdy dzień to czysta karta. Zapisz ją pięknie! 📖",
    "Dzień dobry, skarby! Jesteście super, dacie dziś radę! 💎",
    "Mgła opada, słońce świeci, czas do pracy (lub szkoły) leci! 🎒",
    "Niech ten dzień będzie lepszy od wczorajszego! 🚀",
    "Pozytywna energia wysłana! Łapcie i używajcie! ⚡",
    "Dzień dobry wszystkim nocnym markom i rannym ptaszkom! 🦉",
    "O, już rano? Przeciągamy się i witamy dzień! 🙆‍♀️",
    "Złapcie promienie słońca i naładujcie baterie! 🔋",
    "Jak tam humorki od rana? Mam nadzieję, że wybornie! 🎵",
    "Kawa na stół i lecimy z tym dniem. Dzień dobry! 🚀",
    "Uśmiechnij się! Ktoś na pewno lubi Twój uśmiech. 😁",
    "Dzień dobry, Discordzie! Gotowi na dzisiejsze dramy i memy? 🍿",
    "Szczęśliwego poranka! Niech moc będzie z Wami. ⚔️",
    "Wstawać, nie marudzić! Dzisiaj będzie super! 🌟",
    "Rozbudzamy się powolutku... Dzień dobry! 🥱",
    "Świeży, rześki poranek. Kto by pomyślał, że można wstać tak wcześnie! ⏰",
    "Cudownego dnia, pełnego smacznej kawy i mało stresu! 🍵",
    "Dzień dobry! Pamiętajcie, żeby pić wodę! 💧",
    "Wyspani? Jeśli nie, to czas na drzemkę... Oh wait, do pracy! 💼",
    "Nowy dzień to nowa szansa by zjeść coś dobrego. Smacznego śniadania! 🥞",
    "Czołem! Pamiętajcie o byciu dzisiaj dla siebie życzliwym. 🤝",
    "Zróbcie dzisiaj coś, co sprawi wam radość. Dzień dobry! 🎨",
    "Cześć! Przesyłam mnóstwo wirtualnych przytulasów na start! 🤗",
    "Nadszedł poranek, czas wyruszyć ku nowym przygodom! 🗺️",
    "I znów słońce na niebie. Dzień dobry ekipo! 🌅",
    "Kolejny dzień na serwerze! Cześć wszystkim! 👋",
    "Nie dajcie sobie zepsuć humoru dzisiejszego dnia! 🛡️",
    "Wstajemy! Śniadanko zjedzone? Dzień dobry! 🥐",
    "Kto rano wstaje, temu... bot mówi dzień dobry! 🤖",
    "Dziś jest idealny dzień, żeby nie robić nic... Albo wszystko! Dzień dobry! 🎭",
    "Witam wszystkich milutko! Oby ten dzień był szybki i bezbolesny. 🩺",
    "Budzić się, budzić! Czeka na Was wielki świat! 🌍",
    "Chyba już czas opuścić kołderkowy raj. Dzień dobry! 🛌",
    "Mamy nowy dzień! Czeka nas wiele dobrego. 🍀",
    "Dzień doberek! Gotowi na nowe wyzwania? 🏆",
    "A ku kuku! Kto tam jeszcze śpi? Wstajemy! 👀",
    "Z uśmiechem witamy nowy poranek. Dzień dobry wszystkim! 🌻"
]

NIGHT_MESSAGES = [
    "Dobranoc! Czas zamknąć oczka i odpocząć. 🌙",
    "Słodkich snów! Niech przyśnią Wam się same wspaniałości. 🐑",
    "Kolorowych i puchatych snów wszystkim! ☁️",
    "Czas na sen, odłóżcie telefony! Dobranoc. 📱",
    "Księżyc już świeci, gwiazdy na niebie, czas iść spać! 🌌",
    "Życzę Wam spokojnej, regenerującej nocy. 💤",
    "Pamiętajcie, że jutro też jest dzień. Odpocznijcie! 🛌",
    "Na dziś koniec wrażeń, gasimy światło. Dobranoc! 💡",
    "Śpijcie dobrze moje kotki! 🐾",
    "Cichutko na serwerze, wszyscy idą spać. Prawda? 😉",
    "Niech ta noc przyniesie Wam ukojenie. Do jutra! 🌠",
    "Zadbajcie o dobry sen, jest bardzo ważny. Dobranoc! 🩺",
    "Noc otula świat, czas na wyciszenie. Śpijcie dobrze. 🌃",
    "Jutro będzie nowy, lepszy dzień. A teraz - lulu. 🧸",
    "Słodkich jak miód snów! 🍯",
    "Odpoczywajcie, by rano obudzić się pełni energii! 🔋",
    "Kto późno chodzi spać... ten rano jest zombie. Bierzcie to pod uwagę! 🧟",
    "Spokojnej nocy, wolnej od koszmarów! 🛡️",
    "Zamknijcie oczy, pomyślcie o czymś miłym i zasypiajcie. 🌈",
    "Śpijcie twardo jak kamienie! Tylko wygodniej. 🪨",
    "Czas do łóżka! Kocyk w ruch! 🧣",
    "Ciężki dzień? Sen jest najlepszym lekarstwem. Dobranoc! 💊",
    "Wyśpijcie gorszy humor, jutro wstaniecie jak nowo narodzeni. 🐣",
    "Dobranoc, pchły na noc! A karaluchy pod poduchy! 🪲",
    "Nocna warta bota rozpoczęta, wy możecie iść spać. 🛡️",
    "Nie zapomnijcie nakarmić kota przed snem i dobranoc! 🐈",
    "Serwer idzie powoli spać... Dołączcie do niego. 😴",
    "Trzymajcie się cieplutko pod kocykiem. Dobranoc! 🥶",
    "Każda noc to szansa na ciekawe sny. Oby były epickie! 🎥",
    "Wtulcie się w poduszkę i zapomnijcie o troskach. Dobranoc! ☁️",
    "Puszczam wirtualną kołysankę... Śpijcie dobrze. 🎵",
    "Żegnamy dzisiejszy dzień. Był jaki był, czas na odpoczynek. 🕰️",
    "Ślimaczek chowa się do muszelki, my chowamy się pod kołdrę. Dobranoc! 🐌",
    "Pamiętajcie wyłączyć komputer! Prąd kosztuje 😄 Dobranoc!",
    "Gwiazdy patrzą na Was! Życzę spokojnej nocnej ciszy. 🌟",
    "Dobrej nocki! Pamiętajcie, nie jedzcie w łóżku okruszkami! 🍪",
    "Ciemność spowiła Ziemię, czas na odnowę. Śpijcie dobrze. 🌍",
    "Niech łóżko przypomina Wam najlepszą chmurkę o tej porze. ☁️",
    "Nocne duchy omijają śpiących. Śpijcie cicho! 👻",
    "Skończcie to co robicie i idźcie spać! To rozkaz (ale taki miły). 🫡",
    "Marzenia senne czekają! Do zobaczenia w świecie Morfeusza. 💫",
    "Koniec patrzenia w ekran, oczka też muszą odetchnąć. Dobranoc! 👁️",
    "Dzień się kończy, lecz jutro zaczyna nowy. Spokojnej nocy. 🌅",
    "Sen to darmowe SPA dla ciała i umysłu. Korzystajcie! 🧖‍♀️",
    "Niech sen będzie z Wami! ✨",
    "Do usłyszenia jutro, wyśpijcie się na 100%! 💯",
    "Nieważne co się dziś stało, sen zawsze poprawia sytuację. Dobranoc! 💖",
    "Misiaki przytulone? To idziemy spać. Dobranoc! 🐻",
    "Spokojnego opadania w ramiona snu. Papatki! 👋",
    "Dobranoc wszystkim bez wyjątku. Odpocznijcie sobie porządnie. 🫶"
]

# Strefa czasowa dla Polski (UTC+2)
PL_TZ = datetime.timezone(datetime.timedelta(hours=2))

class DailyGreetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.morning_greeting.start()
        self.night_greeting.start()

    def cog_unload(self):
        self.morning_greeting.cancel()
        self.night_greeting.cancel()

    async def send_random_message(self, messages_list, title, color):
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="💬・pogadanki")
            if channel:
                try:
                    embed = discord.Embed(
                        title=title,
                        description=random.choice(messages_list),
                        color=color
                    )
                    await channel.send(embed=embed)
                except Exception as e:
                    print(f"Błąd wysyłania dziennej wiadomości na {guild.name}: {e}")

    @tasks.loop(time=datetime.time(hour=7, minute=30, tzinfo=PL_TZ))
    async def morning_greeting(self):
        await self.send_random_message(MORNING_MESSAGES, "☀️ Dzień Dobry!", discord.Color.gold())

    @morning_greeting.before_loop
    async def before_morning_greeting(self):
        await self.bot.wait_until_ready()

    @tasks.loop(time=datetime.time(hour=22, minute=0, tzinfo=PL_TZ))
    async def night_greeting(self):
        await self.send_random_message(NIGHT_MESSAGES, "🌙 Dobranoc!", discord.Color.dark_blue())

    @night_greeting.before_loop
    async def before_night_greeting(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(DailyGreetings(bot))
