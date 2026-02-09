import discord
from discord.ext import commands
import random
import asyncio
from utils import get_data, update_data, KAWAII_PINK, KAWAII_GOLD, KAWAII_RED, KAWAII_BLUE

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_balance(self, ctx, amount):
        if amount <= 0:
            embed = discord.Embed(title="❌ Błąd", description="Kwota musi być dodatnia!", color=KAWAII_RED)
            await ctx.send(embed=embed)
            return False

        bal = get_data(ctx.author.id)["balance"]
        if bal < amount:
            embed = discord.Embed(title="💸 Bieda", description=f"Nie masz tyle monet! Masz tylko: **{bal}**", color=KAWAII_RED)
            await ctx.send(embed=embed)
            return False
        return True

    @commands.command(aliases=['slots', 'jednoreki_bandyta'])
    async def maszyna(self, ctx, amount: int):
        """Zagraj w jednorękiego bandytę!"""
        if not await self.check_balance(ctx, amount):
            return

        # Pobieramy kasę na start
        update_data(ctx.author.id, "balance", -amount, "add")

        emojis = ["🍒", "🍋", "🍇", "💎", "7️⃣", "🔔"]

        # Animacja
        msg = await ctx.send("🎰 | 🔄 | 🔄 | 🔄 |")
        await asyncio.sleep(0.5)

        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        # Proste animowanie (edycja wiadomości)
        await msg.edit(content=f"🎰 | {a} | 🔄 | 🔄 |")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎰 | {a} | {b} | 🔄 |")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎰 | {a} | {b} | {c} |")

        # Logika wygranej
        win = 0
        if a == b == c:
            if a == "7️⃣": win = amount * 10
            elif a == "💎": win = amount * 7
            else: win = amount * 5
        elif a == b or b == c or a == c:
            win = int(amount * 1.5)

        embed = discord.Embed(title="🎰 Maszyna Losująca", color=KAWAII_PINK)
        embed.add_field(name="Wynik", value=f"| {a} | {b} | {c} |", inline=False)

        if win > 0:
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 **WYGRANA!** Zgarniasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"❌ Przegrałeś **{amount}** monet. Spróbuj ponownie!"
            embed.color = KAWAII_RED

        await msg.edit(content=None, embed=embed)

    @commands.command(aliases=['rzut', 'flip'])
    async def moneta(self, ctx, amount: int, wybor: str):
        """Rzuć monetą! (orzel/reszka)"""
        if not await self.check_balance(ctx, amount):
            return

        wybor = wybor.lower()
        valid_choices = ["orzel", "reszka", "orzeł"]
        if wybor not in valid_choices:
            await ctx.send("⚠️ Wybierz: `orzel` lub `reszka`!")
            return

        # Normalizacja wyboru
        if wybor == "orzeł": wybor = "orzel"

        update_data(ctx.author.id, "balance", -amount, "add")

        wynik = random.choice(["orzel", "reszka"])

        msg = await ctx.send("🪙 Rzucam monetą...")
        await asyncio.sleep(1)

        embed = discord.Embed(title="🪙 Rzut Monetą", color=KAWAII_GOLD)

        if wynik == wybor:
            win = amount * 2
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"Wypadł **{wynik.upper()}**!\n🎉 Wygrywasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"Wypadł **{wynik.upper()}**.\n❌ Tracisz **{amount}** monet."
            embed.color = KAWAII_RED

        await msg.edit(content=None, embed=embed)

    @commands.command()
    async def ruletka(self, ctx, amount: int, wybor: str):
        """Postaw na kolor (red/black/green) lub liczbę (0-36)"""
        if not await self.check_balance(ctx, amount):
            return

        wybor = wybor.lower()
        valid_colors = ["red", "black", "green", "czerwony", "czarny", "zielony"]

        # Sprawdzanie poprawności wyboru
        is_number = False
        try:
            num = int(wybor)
            if 0 <= num <= 36:
                is_number = True
            else:
                await ctx.send("⚠️ Liczba musi być z zakresu 0-36!")
                return
        except ValueError:
            if wybor not in valid_colors:
                await ctx.send("⚠️ Wybierz kolor (red/black/green) lub liczbę (0-36)!")
                return

        update_data(ctx.author.id, "balance", -amount, "add")

        # Losowanie
        roll = random.randint(0, 36)
        color = "green" if roll == 0 else ("red" if roll % 2 == 1 else "black")

        msg = await ctx.send("🎡 Kręcę kołem...")
        await asyncio.sleep(1.5)

        embed = discord.Embed(title="🎡 Ruletka", color=KAWAII_PINK)
        embed.add_field(name="Wynik", value=f"**{roll}** ({color.upper()})", inline=False)

        win = 0
        if is_number:
            if roll == int(wybor):
                win = amount * 35
        else:
            if wybor in ["red", "czerwony"] and color == "red":
                win = amount * 2
            elif wybor in ["black", "czarny"] and color == "black":
                win = amount * 2
            elif wybor in ["green", "zielony"] and color == "green":
                win = amount * 14

        if win > 0:
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 **WYGRANA!** Zgarniasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"❌ Przegrana. Wynik to {roll} ({color})."
            embed.color = KAWAII_RED

        await msg.edit(content=None, embed=embed)

    @commands.command()
    async def kostka(self, ctx, amount: int):
        """Pojedynek na kości z botem!"""
        if not await self.check_balance(ctx, amount):
            return

        update_data(ctx.author.id, "balance", -amount, "add")

        user_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)

        embed = discord.Embed(title="🎲 Pojedynek na Kości", color=KAWAII_BLUE)
        embed.add_field(name=f"👤 {ctx.author.name}", value=f"🎲 **{user_roll}**", inline=True)
        embed.add_field(name=f"🤖 Bot", value=f"🎲 **{bot_roll}**", inline=True)

        if user_roll > bot_roll:
            win = amount * 2
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 **WYGRANA!** Zgarniasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        elif user_roll < bot_roll:
            embed.description = f"❌ Przegrana. Bot miał więcej oczek!"
            embed.color = KAWAII_RED
        else:
            update_data(ctx.author.id, "balance", amount, "add")
            embed.description = f"🤝 **REMIS!** Odzyskujesz stawkę."
            embed.color = KAWAII_BLUE

        await ctx.send(embed=embed)

    @commands.command()
    async def zgadnij(self, ctx, amount: int, number: int):
        """Zgadnij liczbę od 1 do 10"""
        if not await self.check_balance(ctx, amount):
            return

        if not (1 <= number <= 10):
             await ctx.send("⚠️ Wybierz liczbę od 1 do 10!")
             return

        update_data(ctx.author.id, "balance", -amount, "add")

        winning_number = random.randint(1, 10)

        embed = discord.Embed(title="🔢 Zgadnij Liczbę", color=KAWAII_PINK)

        if number == winning_number:
            win = amount * 5
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 **BRAWO!** Liczba to **{winning_number}**! Wygrywasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"❌ Pudło! Wylosowano **{winning_number}**."
            embed.color = KAWAII_RED

        await ctx.send(embed=embed)

    @commands.command()
    async def wojna(self, ctx, amount: int):
        """Wojna karciana - wyższa karta wygrywa!"""
        if not await self.check_balance(ctx, amount):
            return

        update_data(ctx.author.id, "balance", -amount, "add")

        cards = {
            2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
            11: "J", 12: "Q", 13: "K", 14: "A"
        }

        user_val = random.randint(2, 14)
        bot_val = random.randint(2, 14)

        user_card = cards[user_val]
        bot_card = cards[bot_val]

        embed = discord.Embed(title="⚔️ Wojna Karciana", color=KAWAII_RED)
        embed.add_field(name=f"👤 {ctx.author.name}", value=f"🎴 **{user_card}**", inline=True)
        embed.add_field(name=f"🤖 Bot", value=f"🎴 **{bot_card}**", inline=True)

        if user_val > bot_val:
            win = amount * 2
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 **WYGRANA!** Masz wyższą kartę! +**{win}**"
            embed.color = KAWAII_GOLD
        elif user_val < bot_val:
            embed.description = f"❌ Przegrana. Bot ma wyższą kartę."
            embed.color = KAWAII_RED
        else:
            # Wojna (remis) - prosta wersja: zwrot stawki
            update_data(ctx.author.id, "balance", amount, "add")
            embed.description = f"🤝 **REMIS!** Odzyskujesz stawkę."
            embed.color = KAWAII_BLUE

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
