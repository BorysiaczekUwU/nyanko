import discord
from discord.ext import commands, tasks
import random
import asyncio
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from utils import get_data, update_data, add_item, remove_item, get_market_data, update_market_data, KAWAII_PINK, KAWAII_GOLD, KAWAII_RED, KAWAII_BLUE

SHOP_ROLES = {
    "VIP": 5000,
    "Bogacz": 10000,
    "Słodziak": 2500,
    "Królowa Dram": 3000
}

SHOP_ITEMS = {
    "kick_ticket": {"name": "🎫 Bilet na Kicka", "price": 15000, "desc": "Wyrzuć kogoś raz (nie działa na adminów!)"},
    "mute_ticket": {"name": "🤐 Taśma Klejąca", "price": 5000, "desc": "Wycisz kogoś na 10 min"},
    "unwarn_ticket": {"name": "📜 Czysta Kartoteka", "price": 20000, "desc": "Resetuje twoje przewinienia (RP)"},
    "mystery_box": {"name": "🎁 Tajemnicza Skrzynia", "price": 1000, "desc": "Co jest w środku? (500 - 5000 monet)"},
    "ring": {"name": "💍 Pierścionek Zaręczynowy", "price": 5000, "desc": "Symbol miłości (wymagany do ślubu)"},
    "crown": {"name": "👑 Złota Korona", "price": 100000, "desc": "Prestiżowy przedmiot dla elity"}
}

TYCOON_MACHINES = {
    "koparka": {"name": "⛏️ Koparka Bitcoin", "price": 500, "rate": 10},
    "drukarnia": {"name": "🖨️ Drukarnia", "price": 2000, "rate": 50},
    "mennica": {"name": "🏦 Mennica", "price": 10000, "rate": 250},
    "bank": {"name": "🏛️ Bank Centralny", "price": 50000, "rate": 1500}
}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stock_market_loop.start()

    def cog_unload(self):
        self.stock_market_loop.cancel()

    @tasks.loop(minutes=10)
    async def stock_market_loop(self):
        market = get_market_data()
        companies = market.get("companies", {})

        for ticker, data in companies.items():
            current_price = data["price"]
            # Symulacja: zmiana od -5% do +5%
            change_percent = random.uniform(-0.05, 0.05)
            new_price = round(current_price * (1 + change_percent), 2)
            if new_price < 1.0: new_price = 1.0 # Minimum price

            data["price"] = new_price

            # Historia (max 50 wpisów)
            history = data.get("history", [])
            history.append(new_price)
            if len(history) > 50:
                history.pop(0)
            data["history"] = history

        update_market_data(companies)
        # print("📈 Giełda zaktualizowana!")

    @stock_market_loop.before_loop
    async def before_stock_loop(self):
        await self.bot.wait_until_ready()

    # --- STOCK MARKET COMMANDS ---
    @commands.command()
    async def gielda(self, ctx):
        """Pokaż aktualne kursy akcji"""
        market = get_market_data()
        companies = market.get("companies", {})

        embed = discord.Embed(title="📈 Giełda Kawaii", color=KAWAII_BLUE)
        description = ""

        for ticker, data in companies.items():
            price = data["price"]
            # Oblicz zmiane
            history = data.get("history", [])
            trend = "➖"
            if len(history) >= 2:
                prev = history[-2]
                if price > prev: trend = "🟢 ⬆️"
                elif price < prev: trend = "🔴 ⬇️"

            description += f"**{data['name']} ({ticker})**: `{price} mon` {trend}\n"

        embed.description = description
        embed.set_footer(text="Aktualizacja co 10 min | Użyj !wykres <ticker> aby zobaczyć historię")
        await ctx.send(embed=embed)

    @commands.command()
    async def wykres(self, ctx, ticker: str):
        """Pokaż wykres dla danej firmy"""
        market = get_market_data()
        ticker = ticker.upper()
        companies = market.get("companies", {})

        if ticker not in companies:
            await ctx.send("❌ Nie ma takiej firmy! Dostępne: " + ", ".join(companies.keys()))
            return

        data = companies[ticker]
        history = data.get("history", [])

        if len(history) < 2:
            await ctx.send("⚠️ Za mało danych do wygenerowania wykresu.")
            return

        # Generowanie wykresu matplotlib (OO interface)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(history, marker='o', linestyle='-', color='purple')
        ax.set_title(f"Wykres cen: {data['name']} ({ticker})")
        ax.set_xlabel("Czas")
        ax.set_ylabel("Cena (monety)")
        ax.grid(True)

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        file = discord.File(buf, filename="chart.png")
        embed = discord.Embed(title=f"📈 Wykres {data['name']}", color=KAWAII_BLUE)
        embed.set_image(url="attachment://chart.png")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def kup_akcje(self, ctx, ticker: str, amount: int):
        """Kup akcje firmy"""
        if amount <= 0:
            await ctx.send("❌ Ilość musi być dodatnia!")
            return

        ticker = ticker.upper()
        market = get_market_data()
        companies = market.get("companies", {})

        if ticker not in companies:
            await ctx.send("❌ Nie ma takiej firmy!")
            return

        price = companies[ticker]["price"]
        cost = price * amount

        user_data = get_data(ctx.author.id)
        balance = user_data["balance"]

        if balance < cost:
            await ctx.send(f"💸 Nie stać cię! Koszt: **{round(cost, 2)}**, masz: **{balance}**.")
            return

        # Transakcja
        update_data(ctx.author.id, "balance", -cost, "add")

        # Dodaj akcje
        current_stocks = user_data.get("stocks", {})
        current_stocks[ticker] = current_stocks.get(ticker, 0) + amount
        update_data(ctx.author.id, "stocks", current_stocks, "set")

        await ctx.send(f"📈 Kupiłeś **{amount}** akcji **{ticker}** za **{round(cost, 2)}** monet!")

    @commands.command()
    async def sprzedaj_akcje(self, ctx, ticker: str, amount: int):
        """Sprzedaj akcje firmy"""
        if amount <= 0:
            await ctx.send("❌ Ilość musi być dodatnia!")
            return

        ticker = ticker.upper()
        market = get_market_data()
        companies = market.get("companies", {})

        if ticker not in companies:
            await ctx.send("❌ Nie ma takiej firmy!")
            return

        user_data = get_data(ctx.author.id)
        current_stocks = user_data.get("stocks", {})
        owned = current_stocks.get(ticker, 0)

        if owned < amount:
            await ctx.send(f"❌ Nie masz tyle akcji! Masz: **{owned}**.")
            return

        price = companies[ticker]["price"]
        earnings = price * amount

        # Transakcja
        update_data(ctx.author.id, "balance", earnings, "add")

        current_stocks[ticker] -= amount
        if current_stocks[ticker] == 0:
            del current_stocks[ticker]
        update_data(ctx.author.id, "stocks", current_stocks, "set")

        await ctx.send(f"📉 Sprzedałeś **{amount}** akcji **{ticker}** za **{round(earnings, 2)}** monet!")

    # --- EXISTINING COMMANDS (UPDATED) ---

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def daj_kase(self, ctx, member: discord.Member, amount: int):
        update_data(member.id, "balance", amount, "add")
        await ctx.send(f"💸 **ADMIN:** Dodano **{amount}** monet dla {member.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def zabierz_kase(self, ctx, member: discord.Member, amount: int):
        update_data(member.id, "balance", -amount, "add")
        await ctx.send(f"📉 **ADMIN:** Zabrano **{amount}** monet użytkownikowi {member.mention}!")

    @commands.command()
    async def portfel(self, ctx):
        """Sprawdź swój stan konta i aktywa"""
        try:
            await ctx.message.delete()
        except:
            pass

        data = get_data(ctx.author.id)

        # Ekwipunek
        inv_text = ""
        for item, count in data.get("inventory", {}).items():
            if count > 0:
                name = SHOP_ITEMS.get(item, {}).get("name", item)
                inv_text += f"\n📦 **{name}**: x{count}"
        if not inv_text: inv_text = "\n*(Pusto...)*"
        
        # Akcje
        stocks_text = ""
        market = get_market_data()
        companies = market.get("companies", {})
        total_stock_value = 0

        for ticker, count in data.get("stocks", {}).items():
            if count > 0:
                curr_price = companies.get(ticker, {}).get("price", 0)
                val = count * curr_price
                total_stock_value += val
                stocks_text += f"\n📊 **{ticker}**: {count} szt. (~{round(val)} mon)"

        if not stocks_text: stocks_text = "\n*(Brak akcji)*"

        embed = discord.Embed(title="👛 Twój Portfel", color=KAWAII_GOLD)
        embed.add_field(name="💰 Gotówka", value=f"**{round(data['balance'], 2)}**", inline=True)
        embed.add_field(name="📈 Wartość akcji", value=f"**{round(total_stock_value, 2)}**", inline=True)
        embed.add_field(name="🎒 Plecak", value=inv_text, inline=False)
        embed.add_field(name="💼 Portfolio", value=stocks_text, inline=False)

        try:
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            temp = await ctx.send(f"❌ {ctx.author.mention}, odblokuj DM!")
            await asyncio.sleep(5)
            await temp.delete()

    @commands.command()
    async def daily(self, ctx):
        user_id = ctx.author.id
        data = get_data(user_id)
        now = datetime.now()

        if data.get("last_daily"):
            try:
                last = datetime.fromisoformat(data["last_daily"])
                if now - last < timedelta(hours=24):
                    diff = last + timedelta(hours=24) - now
                    hours, remainder = divmod(diff.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    await ctx.send(f"⏳ Wróć jutro! Za **{hours}h {minutes}m**.")
                    return
            except ValueError:
                pass
        
        update_data(user_id, "balance", 200, "add")
        update_data(user_id, "last_daily", now.isoformat(), "set")

        await ctx.send("🎁 Odebrałeś **200** monet!")

    @commands.command()
    async def sklep(self, ctx):
        embed = discord.Embed(title="🏪 Super Sklep Kawaii", description="Wpisz `!kup <nazwa>`", color=KAWAII_PINK)
        roles_txt = ""
        for r, p in SHOP_ROLES.items(): roles_txt += f"🏷️ **{r}** - `{p}`\n"
        embed.add_field(name="👑 Role", value=roles_txt, inline=False)
        items_txt = ""
        for k, v in SHOP_ITEMS.items(): items_txt += f"📦 **{k}** ({v['name']}) - `{v['price']}`\n*{v['desc']}*\n"
        embed.add_field(name="🛠️ Przedmioty", value=items_txt, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def kup(self, ctx, *, item_name):
        user_id = ctx.author.id
        balance = get_data(user_id)["balance"]
        
        # Kupowanie Ról
        for r, p in SHOP_ROLES.items():
            if r.lower() == item_name.lower():
                if balance < p:
                    await ctx.send("💸 Nie stać cię!")
                    return
                role_obj = discord.utils.get(ctx.guild.roles, name=r)
                if not role_obj:
                    await ctx.send("❌ Rola nie istnieje.")
                    return
                update_data(user_id, "balance", balance - p, "set")
                await ctx.author.add_roles(role_obj)
                await ctx.send(f"🎉 Kupiłeś rolę **{r}**!")
                return

        # Kupowanie Przedmiotów
        if item_name in SHOP_ITEMS:
            item = SHOP_ITEMS[item_name]
            if balance < item["price"]:
                await ctx.send("💸 Nie stać cię!")
                return
            update_data(user_id, "balance", balance - item["price"], "set")
            add_item(user_id, item_name)
            await ctx.send(f"🎒 Kupiłeś **{item['name']}**! Użyj komendą `!uzyj`.")
            return
        
        await ctx.send("❌ Nie ma takiego towaru.")

    @commands.command()
    async def uzyj(self, ctx, item_code, target: discord.Member = None):
        user_id = ctx.author.id
        data = get_data(user_id)
        inventory = data.get("inventory", {})
        
        if inventory.get(item_code, 0) <= 0:
            await ctx.send("❌ Nie masz tego przedmiotu!")
            return

        if item_code == "kick_ticket":
            if not target or target.guild_permissions.administrator:
                await ctx.send("⚠️ Błąd celu (nie podano lub to admin)!")
                return
            remove_item(user_id, item_code)
            try:
                await target.kick(reason="Użycie przedmiotu (Bilet)")
                await ctx.send(f"👋 **{target.name}** wyrzucony biletem!")
            except:
                add_item(user_id, item_code)
                await ctx.send("❌ Błąd bota.")

        elif item_code == "mute_ticket":
            if not target or target.guild_permissions.administrator:
                await ctx.send("⚠️ Błąd celu!")
                return
            remove_item(user_id, item_code)
            await target.timeout(timedelta(minutes=10), reason="Przedmiot (Taśma)")
            await ctx.send(f"🤐 **{target.name}** wyciszony!")

        elif item_code == "unwarn_ticket":
            remove_item(user_id, item_code)
            await ctx.send(f"📜 **{ctx.author.name}** czyści kartotekę!")

        elif item_code == "mystery_box":
            remove_item(user_id, item_code)
            prize = random.randint(500, 5000)
            update_data(user_id, "balance", prize, "add")
            await ctx.send(f"🎁 Otwierasz skrzynię i znajdujesz... **{prize}** monet! 🎉")

        elif item_code == "ring":
            await ctx.send("💍 To piękny pierścionek! Użyj go, aby się oświadczyć komuś (wkrótce!)")

        elif item_code == "crown":
            await ctx.send("👑 Zakładasz koronę i czujesz się jak król! (To tylko przedmiot kosmetyczny)")

    # --- TYCOON COMMANDS ---
    def calculate_tycoon_income(self, user_id):
        data = get_data(user_id)
        tycoon = data.get("tycoon", {})
        machines = tycoon.get("machines", {})
        last_collection = tycoon.get("last_collection")

        # Oblicz rate na godzine
        hourly_rate = 0
        for m_id, count in machines.items():
            if m_id in TYCOON_MACHINES:
                hourly_rate += TYCOON_MACHINES[m_id]["rate"] * count

        if hourly_rate == 0:
            return 0, hourly_rate

        if not last_collection:
            return 0, hourly_rate

        try:
            last_time = datetime.fromisoformat(last_collection)
            now = datetime.now()
            diff = now - last_time
            hours_passed = diff.total_seconds() / 3600
        except:
            return 0, hourly_rate

        # Limit 24h
        if hours_passed > 24:
            hours_passed = 24

        income = int(hourly_rate * hours_passed)
        return income, hourly_rate

    @commands.command()
    async def tycoon(self, ctx):
        """Sprawdź status swojego imperium"""
        data = get_data(ctx.author.id)
        tycoon = data.get("tycoon", {})
        machines = tycoon.get("machines", {})

        income, rate = self.calculate_tycoon_income(ctx.author.id)

        embed = discord.Embed(title="🏭 Twoje Imperium Tycoon", color=KAWAII_PINK)

        machines_text = ""
        for m_id, count in machines.items():
            if count > 0:
                name = TYCOON_MACHINES.get(m_id, {}).get("name", m_id)
                machines_text += f"**{name}**: {count} szt.\n"

        if not machines_text: machines_text = "Brak maszyn. Kup coś w `!sklep_tycoon`!"

        embed.add_field(name="🏭 Maszyny", value=machines_text, inline=False)
        embed.add_field(name="⚡ Produkcja", value=f"**{rate}** mon/h", inline=True)
        embed.add_field(name="💰 Do odebrania", value=f"**{income}** monet", inline=True)
        embed.set_footer(text="Użyj !odbierz aby zgarnąć kasę (max 24h) | !kup_maszyne <nazwa>")

        await ctx.send(embed=embed)

    @commands.command()
    async def sklep_tycoon(self, ctx):
        """Sklep z maszynami"""
        embed = discord.Embed(title="🏭 Sklep Maszyn", description="Zainwestuj, aby zarabiać pasywnie!", color=KAWAII_GOLD)
        for key, val in TYCOON_MACHINES.items():
            embed.add_field(
                name=f"{val['name']} ({key})",
                value=f"💰 Koszt: `{val['price']}`\n⚡ Produkcja: `{val['rate']}/h`",
                inline=False
            )
        embed.set_footer(text="Wpisz !kup_maszyne <nazwa> (np. !kup_maszyne koparka)")
        await ctx.send(embed=embed)

    @commands.command()
    async def kup_maszyne(self, ctx, machine_name: str):
        """Kup maszynę do Tycoona"""
        machine_name = machine_name.lower()
        if machine_name not in TYCOON_MACHINES:
            await ctx.send("❌ Nie ma takiej maszyny!")
            return

        machine = TYCOON_MACHINES[machine_name]
        cost = machine["price"]

        data = get_data(ctx.author.id)
        if data["balance"] < cost:
            await ctx.send(f"💸 Nie stać cię! Potrzebujesz **{cost}** monet.")
            return

        # 1. Oblicz i wypłać zaległy dochód (zabezpieczenie przed exploitem zmiany rate)
        income, _ = self.calculate_tycoon_income(ctx.author.id)
        if income > 0:
            update_data(ctx.author.id, "balance", income, "add")
            await ctx.send(f"💰 Automatycznie odebrano **{income}** monet przed zakupem.")
            # Odśwież dane po wypłacie (balance się zmienił)
            data = get_data(ctx.author.id)

        # Sprawdź ponownie, czy stać po wypłacie (choć income tylko zwiększa balans, więc ok)
        if data["balance"] < cost:
             # Teoretycznie niemożliwe jeśli wcześniej było ok, ale dla pewności
             await ctx.send(f"💸 Nie stać cię! Potrzebujesz **{cost}** monet.")
             return

        # 2. Pobierz koszt
        update_data(ctx.author.id, "balance", -cost, "add")

        # 3. Dodaj maszynę i zresetuj czas
        tycoon = data.get("tycoon", {})
        machines = tycoon.get("machines", {})

        machines[machine_name] = machines.get(machine_name, 0) + 1
        tycoon["machines"] = machines
        tycoon["last_collection"] = datetime.now().isoformat()

        update_data(ctx.author.id, "tycoon", tycoon, "set")

        await ctx.send(f"🏭 Kupiłeś **{machine['name']}**! Twoja produkcja rośnie.")

    @commands.command()
    async def odbierz(self, ctx):
        """Odbierz wyprodukowane pieniądze"""
        income, rate = self.calculate_tycoon_income(ctx.author.id)

        if income <= 0:
            await ctx.send("❌ Nie ma nic do odebrania (lub minęło za mało czasu).")
            return

        update_data(ctx.author.id, "balance", income, "add")

        # Reset czasu
        data = get_data(ctx.author.id)
        tycoon = data.get("tycoon", {})
        tycoon["last_collection"] = datetime.now().isoformat()
        update_data(ctx.author.id, "tycoon", tycoon, "set")

        await ctx.send(f"💰 Odebrano **{income}** monet z produkcji!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
