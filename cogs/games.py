import discord
from discord.ext import commands
import random
import asyncio
from utils import get_data, update_data, KAWAII_PINK, KAWAII_GOLD, KAWAII_RED, KAWAII_BLUE

class BlackjackView(discord.ui.View):
    def __init__(self, bot, player, bet, player_hand, dealer_hand, deck):
        super().__init__(timeout=60)
        self.bot = bot
        self.player = player
        self.bet = bet
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.deck = deck

    def calculate_score(self, hand):
        score = 0
        aces = 0
        for card in hand:
            if card in ["J", "Q", "K"]:
                score += 10
            elif card == "A":
                aces += 1
                score += 11
            else:
                score += int(card)
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def embed_game(self, show_dealer=False):
        embed = discord.Embed(title="🃏 Blackjack", color=KAWAII_BLUE)
        
        d_score = self.calculate_score(self.dealer_hand) if show_dealer else "?"
        d_cards = " ".join(self.dealer_hand) if show_dealer else f"{self.dealer_hand[0]} ?"
        
        p_score = self.calculate_score(self.player_hand)
        p_cards = " ".join(self.player_hand)
        
        embed.add_field(name=f"Krupier ({d_score})", value=d_cards, inline=False)
        embed.add_field(name=f"Gracz ({p_score})", value=p_cards, inline=False)
        return embed

    async def end_game(self, interaction, result, score):
        for child in self.children:
            child.disabled = True
        
        embed = self.embed_game(show_dealer=True)
        if result == "win":
            win = self.bet * 2
            update_data(self.player.id, "balance", win, "add")
            embed.description = f"🎉 Wygrywasz! (Zgarniasz **{win}**)"
            embed.color = KAWAII_GOLD
        elif result == "bj":
            win = int(self.bet * 2.5)
            update_data(self.player.id, "balance", win, "add")
            embed.description = f"🔥 BLACKJACK! (Zgarniasz **{win}**)"
            embed.color = KAWAII_GOLD
        elif result == "lose":
            embed.description = f"❌ Przegrywasz **{self.bet}**."
            embed.color = KAWAII_RED
        elif result == "tie":
            update_data(self.player.id, "balance", self.bet, "add")
            embed.description = f"🤝 Remis! Odzyskujesz stawkę."
            
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Dobierz (Hit)", style=discord.ButtonStyle.primary)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id: return
        self.player_hand.append(self.deck.pop())
        score = self.calculate_score(self.player_hand)
        
        if score > 21:
            await self.end_game(interaction, "lose", score)
        elif score == 21:
            await self.stand(interaction, button)
        else:
            await interaction.response.edit_message(embed=self.embed_game(), view=self)

    @discord.ui.button(label="Czekaj (Stand)", style=discord.ButtonStyle.danger)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction and interaction.user.id != self.player.id: return
        
        p_score = self.calculate_score(self.player_hand)
        d_score = self.calculate_score(self.dealer_hand)
        
        while d_score < 17:
            self.dealer_hand.append(self.deck.pop())
            d_score = self.calculate_score(self.dealer_hand)
            
        if d_score > 21 or p_score > d_score:
            await self.end_game(interaction, "win", p_score)
        elif d_score > p_score:
            await self.end_game(interaction, "lose", p_score)
        else:
            await self.end_game(interaction, "tie", p_score)

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

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx, amount: int):
        """Zagraj w Blackjacka!"""
        if not await self.check_balance(ctx, amount): return
        
        update_data(ctx.author.id, "balance", -amount, "add")
        
        deck = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"] * 4
        random.shuffle(deck)
        
        p_hand = [deck.pop(), deck.pop()]
        d_hand = [deck.pop(), deck.pop()]
        
        view = BlackjackView(self.bot, ctx.author, amount, p_hand, d_hand, deck)
        
        p_score = view.calculate_score(p_hand)
        if p_score == 21:
            v = view.embed_game(show_dealer=True)
            win = int(amount * 2.5)
            update_data(ctx.author.id, "balance", win, "add")
            v.description = f"🔥 BLACKJACK! Zgarniasz **{win}** monet!"
            v.color = KAWAII_GOLD
            await ctx.send(embed=v)
        else:
            await ctx.send(embed=view.embed_game(), view=view)

async def setup(bot):
    await bot.add_cog(Games(bot))
