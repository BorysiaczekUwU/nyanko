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

class MineView(discord.ui.View):
    def __init__(self, bot, player, bet, mines_count):
        super().__init__(timeout=60)
        self.bot = bot
        self.player = player
        self.bet = bet
        self.mines_count = mines_count
        
        self.board_size = 20
        self.mines = random.sample(range(self.board_size), self.mines_count)
        self.revealed = 0
        self.multiplier = 1.0
        self.active = True
        
        for i in range(self.board_size):
            btn = discord.ui.Button(label="❓", style=discord.ButtonStyle.secondary, custom_id=str(i), row=i//5)
            btn.callback = self.make_callback(i, btn)
            self.add_item(btn)
            
        self.cashout_btn = discord.ui.Button(label="Wypłać: 0.0x", style=discord.ButtonStyle.success, custom_id="cashout", row=4)
        self.cashout_btn.callback = self.cashout_callback
        self.cashout_btn.disabled = True
        self.add_item(self.cashout_btn)

    def calculate_multiplier(self):
        safe_left = 20 - self.mines_count - self.revealed
        total_left = 20 - self.revealed
        if total_left <= 0: return self.multiplier
        step_mult = total_left / max(1, safe_left)
        return round(self.multiplier * step_mult * 0.95, 2)

    def make_callback(self, index, button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.player.id: return
            if not self.active: return

            if index in self.mines:
                self.active = False
                self.reveal_all(interaction)
                await self.end_game(interaction, False)
            else:
                button.label = "💎"
                button.style = discord.ButtonStyle.success
                button.disabled = True
                self.revealed += 1
                
                if self.revealed == 1:
                    self.multiplier = round(20 / (20 - self.mines_count) * 0.95, 2)
                    self.cashout_btn.disabled = False
                else:
                    self.multiplier = self.calculate_multiplier()
                
                self.cashout_btn.label = f"Wypłać: {self.multiplier}x"
                
                if self.revealed == (20 - self.mines_count):
                    self.active = False
                    self.reveal_all(interaction)
                    await self.end_game(interaction, True)
                else:
                    await interaction.response.edit_message(embed=self.embed_game(), view=self)
        return callback

    async def cashout_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.player.id: return
        if not self.active: return
        self.active = False
        self.reveal_all(interaction)
        await self.end_game(interaction, True)

    def reveal_all(self, interaction):
        for item in self.children:
            item.disabled = True
            if item.custom_id and item.custom_id.isdigit():
                idx = int(item.custom_id)
                if idx in self.mines:
                    item.label = "💥"
                    item.style = discord.ButtonStyle.danger
                elif item.label == "❓":
                    item.label = "💎"
                    item.style = discord.ButtonStyle.secondary

    def embed_game(self):
        embed = discord.Embed(title="💣 Mines", color=KAWAII_BLUE)
        embed.add_field(name="Stawka", value=f"**{self.bet}**", inline=True)
        embed.add_field(name="Miny", value=f"**{self.mines_count}**", inline=True)
        embed.add_field(name="Obecny Mnożnik", value=f"**{self.multiplier}x**", inline=True)
        return embed

    async def end_game(self, interaction, won):
        embed = self.embed_game()
        if won:
            win_amount = int(self.bet * self.multiplier)
            update_data(self.player.id, "balance", win_amount, "add")
            embed.description = f"🎉 Wypłacasz i wygrywasz **{win_amount}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"💥 Boom! Trafiłeś na minę i tracisz **{self.bet}** monet."
            embed.color = KAWAII_RED
        await interaction.response.edit_message(embed=embed, view=self)

class PokerView(discord.ui.View):
    def __init__(self, bot, player, bet, deck):
        super().__init__(timeout=60)
        self.bot = bot
        self.player = player
        self.bet = bet
        self.deck = deck
        
        self.p_hand = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        self.d_hand = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        
    def evaluate_hand(self, hand):
        values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
        hand_vals = sorted([values[c] for c in hand], reverse=True)
        counts = {v: hand_vals.count(v) for v in hand_vals}
        
        if 3 in counts.values(): return 300 + hand_vals[0]
        if 2 in counts.values():
            pair_val = [k for k, v in counts.items() if v == 2][0]
            kicker = [k for k in hand_vals if k != pair_val][0]
            return 100 + pair_val * 10 + kicker
        return hand_vals[0] * 100 + hand_vals[1] * 10 + hand_vals[2]

    def embed_game(self, show_dealer=False):
        embed = discord.Embed(title="🃏 3 Card Poker", color=KAWAII_BLUE)
        d_cards = " ".join(self.d_hand) if show_dealer else f"{self.d_hand[0]} ❓ ❓"
        p_cards = " ".join(self.p_hand)
        embed.add_field(name=f"Krupier", value=d_cards, inline=False)
        embed.add_field(name=f"Gracz", value=p_cards, inline=False)
        return embed

    async def end_game(self, interaction, action):
        for child in self.children:
            child.disabled = True
            
        embed = self.embed_game(show_dealer=True)
        
        if action == "fold":
            embed.description = f"🏳️ Pasujesz. Tracisz stawkę **{self.bet}** monet."
            embed.color = KAWAII_RED
        else:
            p_score = self.evaluate_hand(self.p_hand)
            d_score = self.evaluate_hand(self.d_hand)
            
            if p_score > d_score:
                win = self.bet * 2
                update_data(self.player.id, "balance", win, "add")
                embed.description = f"🎉 Wygrywasz! (Zgarniasz **{win}**)"
                embed.color = KAWAII_GOLD
            elif p_score < d_score:
                update_data(self.player.id, "balance", -self.bet, "add")
                embed.description = f"❌ Przegrywasz. Tracisz dodatkowe **{self.bet}** (razem **{self.bet*2}**)."
                embed.color = KAWAII_RED
            else:
                update_data(self.player.id, "balance", self.bet, "add")
                embed.description = f"🤝 Remis! Odzyskujesz pierwotną stawkę."
                
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Graj (x2 stawka)", style=discord.ButtonStyle.success)
    async def play_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id: return
        bal = get_data(self.player.id)["balance"]
        if bal < self.bet:
            return await interaction.response.send_message("❌ Nie masz wystarczająco monet, by podbić i grać!", ephemeral=True)
        await self.end_game(interaction, "play")

    @discord.ui.button(label="Pas (Fold)", style=discord.ButtonStyle.danger)
    async def fold_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id: return
        await self.end_game(interaction, "fold")

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

    @commands.command(aliases=['scratch'])
    async def zdrapka(self, ctx, amount: int):
        """Kup zdrapkę i wygraj kasę!"""
        if not await self.check_balance(ctx, amount): return
        
        update_data(ctx.author.id, "balance", -amount, "add")
        
        emojis = ["🍒", "🍋", "💸", "💎", "⭐"]
        e1, e2, e3 = random.choices(emojis, k=3)
        
        win = 0
        if e1 == e2 == e3:
            win = amount * 5
        elif e1 == e2 or e2 == e3 or e1 == e3:
            win = int(amount * 1.5)
            
        embed = discord.Embed(title="🎟️ Zdrapka Kawaii", color=KAWAII_PINK)
        embed.description = f"Zdrapek kosztuje: **{amount}** monet. Oto twój wynik:\n\n"
        embed.description += f"|| {e1} || || {e2} || || {e3} ||"
        
        if win > 0:
            update_data(ctx.author.id, "balance", win, "add")
            embed.add_field(name="Wynik", value=f"🎉 Wygrywasz **{win}** monet!", inline=False)
            embed.color = KAWAII_GOLD
        else:
            embed.add_field(name="Wynik", value=f"❌ Niestety, nic nie wygrywasz.", inline=False)
            embed.color = KAWAII_RED
            
        await ctx.send(embed=embed)

    @commands.command()
    async def wyscig(self, ctx, amount: int, animal: str):
        """Obstawiaj wyścigi! (zolw, krolik, pies, kot)"""
        if not await self.check_balance(ctx, amount): return
        
        valid_animals = {"zolw": "🐢", "krolik": "🐰", "pies": "🐶", "kot": "🐱"}
        animal = animal.lower()
        if animal not in valid_animals:
            return await ctx.send("⚠️ Wybierz zawodnika: `zolw`, `krolik`, `pies`, lub `kot`.")
            
        update_data(ctx.author.id, "balance", -amount, "add")
        
        msg = await ctx.send("🏁 Wyścig się rozpoczyna...")
        await asyncio.sleep(2)
        
        winner_key = random.choice(list(valid_animals.keys()))
        winner_emoji = valid_animals[winner_key]
        
        embed = discord.Embed(title="🏁 Tor Wyścigowy", color=KAWAII_BLUE)
        embed.description = f"Twój faworyt: {valid_animals[animal]}\nZwycięzca na macie to... **{winner_emoji} {winner_key.upper()}**!"
        
        if animal == winner_key:
            win = int(amount * 3.5)
            update_data(ctx.author.id, "balance", win, "add")
            embed.add_field(name="Wynik", value=f"🎉 Twój pupil wygrywa! Zgarniasz **{win}** monet!", inline=False)
            embed.color = KAWAII_GOLD
        else:
            embed.add_field(name="Wynik", value=f"❌ Twój pupil przegrał. Tracisz stawkę.", inline=False)
            embed.color = KAWAII_RED
            
        await msg.edit(content=None, embed=embed)

    @commands.command()
    async def kubki(self, ctx, amount: int, cup: int):
        """Zgadnij gdzie jest piłeczka! (wybierz kubek 1, 2 lub 3)"""
        if not await self.check_balance(ctx, amount): return
        
        if cup not in [1, 2, 3]:
            return await ctx.send("⚠️ Musisz wybrać kubek: `1`, `2` lub `3`.")
            
        update_data(ctx.author.id, "balance", -amount, "add")
        
        winning_cup = random.randint(1, 3)
        cups_display = ["🥤", "🥤", "🥤"]
        cups_display[winning_cup - 1] = "🎱"  # pokazuje gdzie byla pila
        
        embed = discord.Embed(title="🥤 Gra w Trzy Kubki", color=KAWAII_GOLD)
        embed.description = f"Obstawiałeś kubek nr **{cup}**.\n\nWynik: " + " ".join(cups_display)
        
        if cup == winning_cup:
            win = int(amount * 2.5)
            update_data(ctx.author.id, "balance", win, "add")
            embed.add_field(name="Wynik", value=f"🎉 Znalazłeś piłeczkę! Wygrywasz **{win}** monet!", inline=False)
        else:
            embed.add_field(name="Wynik", value=f"❌ Pusto! Tracisz stawkę.", inline=False)
            embed.color = KAWAII_RED
            
        await ctx.send(embed=embed)

    @commands.command()
    async def mines(self, ctx, amount: int, mines_count: int):
        """Zagraj w sapera! Wybierz ilość min od 1 do 19"""
        if not await self.check_balance(ctx, amount): return
        if not 1 <= mines_count <= 19:
            return await ctx.send("⚠️ Wybierz między 1 a 19 min!")
            
        update_data(ctx.author.id, "balance", -amount, "add")
        
        view = MineView(self.bot, ctx.author, amount, mines_count)
        await ctx.send("💣 Odkrywaj pola ostrożnie...", embed=view.embed_game(), view=view)

    @commands.command()
    async def poker(self, ctx, amount: int):
        """Zagraj w 3-Card Poker!"""
        if not await self.check_balance(ctx, amount): return
        
        update_data(ctx.author.id, "balance", -amount, "add")
        
        deck = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"] * 4
        random.shuffle(deck)
        
        view = PokerView(self.bot, ctx.author, amount, deck)
        await ctx.send("Krupier rozdaje po 3 karty...", embed=view.embed_game(), view=view)

    @commands.command()
    async def crash(self, ctx, amount: int, cel: float):
        """Gra Crash! Obstaw stawkę i cel mnożnika (np. 1.5)"""
        if not await self.check_balance(ctx, amount): return
        if cel <= 1.0:
            return await ctx.send("⚠️ Minimalny cel to >1.01x!")

        update_data(ctx.author.id, "balance", -amount, "add")

        msg = await ctx.send("🚀 Rakieta startuje...")
        
        if random.random() < 0.05:
            crash_point = 1.0
        else:
            crash_point = round(max(1.01, 0.99 / random.random()), 2)
            
        await asyncio.sleep(2)
        
        embed = discord.Embed(title="🚀 Crash", color=KAWAII_BLUE)
        embed.add_field(name="Twój cel", value=f"**{cel}x**", inline=True)
        embed.add_field(name="Crash", value=f"**{crash_point}x**", inline=True)
        
        if crash_point >= cel:
            win = int(amount * cel)
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 Zdążyłeś! Wygrywasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"💥 Boom! Rakieta rozbiła się za wcześnie. Tracisz **{amount}** monet."
            embed.color = KAWAII_RED
            
        await msg.edit(content=None, embed=embed)

    @commands.command()
    async def kolofortuny(self, ctx, amount: int, wybor: str):
        """Zakręć Kołem! (wybierz: zielony, czerwony, niebieski, zloty)"""
        if not await self.check_balance(ctx, amount): return
        
        valid = {"zielony": 2, "czerwony": 2, "niebieski": 3, "zloty": 10}
        wybor = wybor.lower()
        if wybor not in valid:
            return await ctx.send("⚠️ Wybierz: `zielony` (x2), `czerwony` (x2), `niebieski` (x3), `zloty` (x10).")
            
        update_data(ctx.author.id, "balance", -amount, "add")
        
        msg = await ctx.send("🎡 Kręcę Kołem Fortuny...")
        await asyncio.sleep(2)
        
        pule = ["zielony"]*40 + ["czerwony"]*40 + ["niebieski"]*15 + ["zloty"]*5
        wynik = random.choice(pule)
        
        embed = discord.Embed(title="🎡 Koło Fortuny", color=KAWAII_PINK)
        embed.add_field(name="Wynik", value=f"Wypadł kolor: **{wynik.upper()}**", inline=False)
        
        if wybor == wynik:
            win = amount * valid[wynik]
            update_data(ctx.author.id, "balance", win, "add")
            embed.description = f"🎉 Zgadłeś! Wygrywasz **{win}** monet!"
            embed.color = KAWAII_GOLD
        else:
            embed.description = f"❌ Nie zgadłeś. Tracisz **{amount}** monet."
            embed.color = KAWAII_RED
            
        await msg.edit(content=None, embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))
